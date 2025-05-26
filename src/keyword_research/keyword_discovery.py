#!/usr/bin/env python3
"""
Keyword Discovery Engine for SEO Affiliate Content Site
Automated keyword research using Google Autocomplete, SerpAPI, and other sources.
"""

import asyncio
import aiohttp
import json
import random
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus
import yaml
from pathlib import Path
from loguru import logger

from config.settings import settings

class KeywordDiscovery:
    """Automated keyword discovery and research engine."""
    
    def __init__(self):
        self.serpapi_key = settings.SERPAPI_KEY
        self.google_api_key = settings.GOOGLE_API_KEY
        
        # Load keyword configuration
        self.keyword_config = self._load_keyword_config()
        
        # Session for HTTP requests
        self.session = None
    
    def _load_keyword_config(self) -> Dict[str, Any]:
        """Load keyword configuration from YAML file."""
        config_path = settings.PROJECT_ROOT / "config" / "keywords.yaml"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading keyword config: {e}")
            return {}
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def discover_keywords(self, count: int = 50) -> List[Dict[str, Any]]:
        """Discover new keywords using multiple sources."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            all_keywords = []
            
            # Generate keywords from patterns
            pattern_keywords = await self._generate_pattern_keywords(count // 3)
            all_keywords.extend(pattern_keywords)
            
            # Get Google Autocomplete suggestions
            autocomplete_keywords = await self._get_autocomplete_keywords(count // 3)
            all_keywords.extend(autocomplete_keywords)
            
            # Get SerpAPI keyword data
            serpapi_keywords = await self._get_serpapi_keywords(count // 3)
            all_keywords.extend(serpapi_keywords)
            
            # Remove duplicates and filter
            unique_keywords = self._deduplicate_keywords(all_keywords)
            filtered_keywords = self._filter_keywords(unique_keywords)
            
            # Sort by potential value
            sorted_keywords = self._sort_keywords_by_value(filtered_keywords)
            
            return sorted_keywords[:count]
            
        except Exception as e:
            logger.error(f"Error in keyword discovery: {e}")
            return []
        finally:
            if self.session:
                await self.session.close()
                self.session = None
    
    async def _generate_pattern_keywords(self, count: int) -> List[Dict[str, Any]]:
        """Generate keywords using predefined patterns."""
        keywords = []
        patterns = self.keyword_config.get('keyword_patterns', [])
        
        if not patterns:
            return keywords
        
        # Get categories and audiences
        categories = list(self.keyword_config.get('seed_keywords', {}).keys())
        audiences = self.keyword_config.get('target_audiences', [])
        
        # Load affiliate tools
        affiliate_config_path = settings.PROJECT_ROOT / "config" / "affiliate_links.yaml"
        try:
            with open(affiliate_config_path, 'r', encoding='utf-8') as f:
                affiliate_data = yaml.safe_load(f)
                tools = list(affiliate_data.keys())
        except:
            tools = ['hubspot', 'convertkit', 'asana', 'canva']
        
        for _ in range(count):
            try:
                pattern = random.choice(patterns)
                category = random.choice(categories)
                audience = random.choice(audiences)
                tool = random.choice(tools)
                
                # Replace placeholders
                keyword = pattern.format(
                    tool_category=category.replace('_', ' '),
                    audience=audience,
                    tool_name=tool,
                    competitor=random.choice(tools)
                )
                
                keywords.append({
                    'keyword': keyword,
                    'source': 'pattern_generation',
                    'category': category,
                    'target_audience': audience,
                    'search_intent': self._classify_search_intent(keyword),
                    'search_volume': random.randint(100, 1000),  # Placeholder
                    'keyword_difficulty': random.randint(10, 40),  # Placeholder
                    'competition_level': 'low'
                })
                
            except Exception as e:
                logger.debug(f"Error generating pattern keyword: {e}")
                continue
        
        return keywords
    
    async def _get_autocomplete_keywords(self, count: int) -> List[Dict[str, Any]]:
        """Get keyword suggestions from Google Autocomplete."""
        keywords = []
        
        if not self.session:
            return keywords
        
        # Get seed keywords
        seed_keywords = []
        for category_seeds in self.keyword_config.get('seed_keywords', {}).values():
            seed_keywords.extend(category_seeds[:3])  # Take first 3 from each category
        
        for seed in seed_keywords[:10]:  # Limit to 10 seeds
            try:
                suggestions = await self._fetch_autocomplete_suggestions(seed)
                
                for suggestion in suggestions[:5]:  # Take top 5 suggestions per seed
                    keywords.append({
                        'keyword': suggestion,
                        'source': 'google_autocomplete',
                        'category': self._categorize_keyword(suggestion),
                        'target_audience': 'general',
                        'search_intent': self._classify_search_intent(suggestion),
                        'search_volume': 0,  # Will be filled by SerpAPI if available
                        'keyword_difficulty': 0,
                        'competition_level': 'unknown'
                    })
                
                # Add delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.debug(f"Error getting autocomplete for '{seed}': {e}")
                continue
        
        return keywords[:count]
    
    async def _fetch_autocomplete_suggestions(self, seed_keyword: str) -> List[str]:
        """Fetch autocomplete suggestions from Google."""
        url = "http://suggestqueries.google.com/complete/search"
        params = {
            'client': 'firefox',
            'q': seed_keyword
        }
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    text = await response.text()
                    # Parse the JSONP response
                    if text.startswith('window.google.ac.h('):
                        json_str = text[19:-1]  # Remove JSONP wrapper
                        data = json.loads(json_str)
                        return data[1] if len(data) > 1 else []
                    else:
                        # Try parsing as regular JSON
                        data = json.loads(text)
                        return data[1] if len(data) > 1 else []
        except Exception as e:
            logger.debug(f"Error fetching autocomplete for '{seed_keyword}': {e}")
        
        return []
    
    async def _get_serpapi_keywords(self, count: int) -> List[Dict[str, Any]]:
        """Get keyword data from SerpAPI."""
        keywords = []
        
        if not self.serpapi_key or not self.session:
            return keywords
        
        # Get some seed keywords for SerpAPI research
        seed_keywords = []
        for category_seeds in self.keyword_config.get('seed_keywords', {}).values():
            seed_keywords.extend(category_seeds[:2])
        
        for seed in seed_keywords[:5]:  # Limit API calls
            try:
                keyword_data = await self._fetch_serpapi_data(seed)
                keywords.extend(keyword_data)
                
                # Add delay to respect rate limits
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.debug(f"Error getting SerpAPI data for '{seed}': {e}")
                continue
        
        return keywords[:count]
    
    async def _fetch_serpapi_data(self, keyword: str) -> List[Dict[str, Any]]:
        """Fetch keyword data from SerpAPI."""
        url = "https://serpapi.com/search"
        params = {
            'engine': 'google_keyword',
            'q': keyword,
            'api_key': self.serpapi_key,
            'data_type': 'json'
        }
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    keywords = []
                    
                    # Extract related keywords
                    if 'related_keywords' in data:
                        for related in data['related_keywords'][:10]:
                            keywords.append({
                                'keyword': related.get('keyword', ''),
                                'source': 'serpapi',
                                'category': self._categorize_keyword(related.get('keyword', '')),
                                'target_audience': 'general',
                                'search_intent': self._classify_search_intent(related.get('keyword', '')),
                                'search_volume': related.get('monthly_searches', 0),
                                'keyword_difficulty': related.get('competition', 0),
                                'competition_level': self._map_competition_level(related.get('competition', 0))
                            })
                    
                    return keywords
                    
        except Exception as e:
            logger.debug(f"Error fetching SerpAPI data for '{keyword}': {e}")
        
        return []
    
    def _deduplicate_keywords(self, keywords: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate keywords."""
        seen = set()
        unique_keywords = []
        
        for keyword_data in keywords:
            keyword = keyword_data['keyword'].lower().strip()
            if keyword and keyword not in seen:
                seen.add(keyword)
                keyword_data['keyword'] = keyword
                unique_keywords.append(keyword_data)
        
        return unique_keywords
    
    def _filter_keywords(self, keywords: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter keywords based on criteria."""
        filtered = []
        criteria = self.keyword_config.get('filtering_criteria', {})
        
        min_search_volume = criteria.get('min_search_volume', 0)
        max_keyword_difficulty = criteria.get('max_keyword_difficulty', 100)
        min_word_count = criteria.get('min_word_count', 2)
        max_word_count = criteria.get('max_word_count', 10)
        exclude_patterns = criteria.get('exclude_patterns', [])
        
        for keyword_data in keywords:
            keyword = keyword_data['keyword']
            
            # Check word count
            word_count = len(keyword.split())
            if word_count < min_word_count or word_count > max_word_count:
                continue
            
            # Check search volume
            if keyword_data.get('search_volume', 0) < min_search_volume:
                continue
            
            # Check keyword difficulty
            if keyword_data.get('keyword_difficulty', 0) > max_keyword_difficulty:
                continue
            
            # Check exclude patterns
            if any(pattern.lower() in keyword.lower() for pattern in exclude_patterns):
                continue
            
            filtered.append(keyword_data)
        
        return filtered
    
    def _sort_keywords_by_value(self, keywords: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort keywords by potential value (search volume / difficulty)."""
        def keyword_value(keyword_data):
            volume = keyword_data.get('search_volume', 100)
            difficulty = max(keyword_data.get('keyword_difficulty', 20), 1)
            return volume / difficulty
        
        return sorted(keywords, key=keyword_value, reverse=True)
    
    def _categorize_keyword(self, keyword: str) -> str:
        """Categorize a keyword based on content."""
        keyword_lower = keyword.lower()
        
        category_keywords = {
            'crm_tools': ['crm', 'customer relationship', 'sales automation', 'lead management'],
            'email_marketing': ['email', 'newsletter', 'mailchimp', 'convertkit'],
            'project_management': ['project', 'task', 'asana', 'monday', 'collaboration'],
            'design_tools': ['design', 'canva', 'figma', 'logo', 'graphic'],
            'analytics_tools': ['analytics', 'tracking', 'data', 'metrics'],
            'automation_tools': ['automation', 'zapier', 'workflow', 'integration']
        }
        
        for category, category_terms in category_keywords.items():
            if any(term in keyword_lower for term in category_terms):
                return category
        
        return 'general'
    
    def _classify_search_intent(self, keyword: str) -> str:
        """Classify the search intent of a keyword."""
        keyword_lower = keyword.lower()
        
        intent_patterns = self.keyword_config.get('search_intent', {})
        
        for intent, patterns in intent_patterns.items():
            if any(pattern in keyword_lower for pattern in patterns):
                return intent
        
        return 'informational'
    
    def _map_competition_level(self, competition_score: float) -> str:
        """Map numeric competition score to level."""
        if competition_score <= 0.3:
            return 'low'
        elif competition_score <= 0.7:
            return 'medium'
        else:
            return 'high'
