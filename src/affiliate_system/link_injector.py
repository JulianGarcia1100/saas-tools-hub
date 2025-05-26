#!/usr/bin/env python3
"""
Affiliate Link Injector for SEO Affiliate Content Site
Intelligently injects contextual affiliate links into generated content.
"""

import re
import random
import yaml
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from loguru import logger

from config.settings import settings

class AffiliateInjector:
    """Intelligently injects affiliate links into content."""
    
    def __init__(self):
        self.affiliate_data = self._load_affiliate_data()
        self.link_density = settings.AFFILIATE_LINK_DENSITY
        self.cta_variations = settings.CTA_VARIATIONS
    
    def _load_affiliate_data(self) -> Dict[str, Any]:
        """Load affiliate links configuration."""
        affiliate_config_path = settings.PROJECT_ROOT / "config" / "affiliate_links.yaml"
        
        try:
            with open(affiliate_config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading affiliate data: {e}")
            return {}
    
    async def inject_links(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inject affiliate links into content."""
        try:
            content = content_data['content']
            category = content_data.get('category', 'general')
            
            # Find relevant tools mentioned in content
            mentioned_tools = self._find_mentioned_tools(content)
            
            # Get contextual affiliate opportunities
            opportunities = self._find_affiliate_opportunities(content, category)
            
            # Inject affiliate links
            updated_content = self._inject_contextual_links(content, mentioned_tools, opportunities)
            
            # Add CTA blocks
            updated_content = self._add_cta_blocks(updated_content, category)
            
            # Count affiliate links
            affiliate_count = self._count_affiliate_links(updated_content)
            
            # Update content data
            content_data['content'] = updated_content
            content_data['affiliate_links_count'] = affiliate_count
            
            logger.info(f"Injected {affiliate_count} affiliate links into content")
            return content_data
            
        except Exception as e:
            logger.error(f"Error injecting affiliate links: {e}")
            return content_data
    
    def _find_mentioned_tools(self, content: str) -> List[Dict[str, Any]]:
        """Find tools mentioned in the content."""
        mentioned_tools = []
        content_lower = content.lower()
        
        for tool_key, tool_data in self.affiliate_data.items():
            if tool_key == 'default_ctas':
                continue
            
            tool_name = tool_data.get('name', '').lower()
            keywords = tool_data.get('keywords', [])
            
            # Check if tool name is mentioned
            if tool_name in content_lower:
                mentioned_tools.append({
                    'key': tool_key,
                    'data': tool_data,
                    'mentions': content_lower.count(tool_name)
                })
                continue
            
            # Check if any keywords are mentioned
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    mentioned_tools.append({
                        'key': tool_key,
                        'data': tool_data,
                        'mentions': content_lower.count(keyword.lower())
                    })
                    break
        
        # Sort by number of mentions
        mentioned_tools.sort(key=lambda x: x['mentions'], reverse=True)
        return mentioned_tools
    
    def _find_affiliate_opportunities(self, content: str, category: str) -> List[Dict[str, Any]]:
        """Find opportunities to inject affiliate links."""
        opportunities = []
        
        # Get relevant tools for this category
        relevant_tools = self._get_relevant_tools(category)
        
        # Find sentences that could benefit from tool recommendations
        sentences = re.split(r'[.!?]+', content)
        
        opportunity_patterns = [
            r'\b(need|want|looking for|searching for|require)\b.*\b(tool|software|platform|solution|app)\b',
            r'\b(best|top|recommended|popular)\b.*\b(tool|software|platform|solution)\b',
            r'\b(help|assist|support|manage|organize|automate)\b',
            r'\b(productivity|efficiency|workflow|collaboration)\b',
            r'\b(small business|startup|freelancer|entrepreneur)\b'
        ]
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if len(sentence) < 20:  # Skip very short sentences
                continue
            
            for pattern in opportunity_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    opportunities.append({
                        'sentence_index': i,
                        'sentence': sentence,
                        'pattern': pattern,
                        'relevant_tools': relevant_tools[:3]  # Top 3 relevant tools
                    })
                    break
        
        return opportunities[:5]  # Limit opportunities
    
    def _inject_contextual_links(self, content: str, mentioned_tools: List[Dict[str, Any]], opportunities: List[Dict[str, Any]]) -> str:
        """Inject contextual affiliate links into content."""
        updated_content = content
        
        # Replace tool mentions with affiliate links
        for tool_info in mentioned_tools[:3]:  # Limit to top 3 mentioned tools
            tool_data = tool_info['data']
            tool_name = tool_data['name']
            affiliate_url = tool_data['affiliate_url']
            
            # Create affiliate link
            affiliate_link = f"[{tool_name}]({affiliate_url})"
            
            # Replace first mention with link (case-insensitive)
            pattern = re.compile(re.escape(tool_name), re.IGNORECASE)
            updated_content = pattern.sub(affiliate_link, updated_content, count=1)
        
        return updated_content
    
    def _add_cta_blocks(self, content: str, category: str) -> str:
        """Add call-to-action blocks throughout the content."""
        # Get relevant tools for CTAs
        relevant_tools = self._get_relevant_tools(category)
        
        if not relevant_tools:
            return content
        
        # Split content into sections (by H2 headings)
        sections = re.split(r'\n## ', content)
        
        if len(sections) < 2:
            # No H2 headings, add CTA at the end
            return content + "\n\n" + self._generate_cta_block(relevant_tools[0])
        
        updated_sections = [sections[0]]  # Keep the first section as-is
        
        # Add CTA blocks after every 2-3 sections
        for i, section in enumerate(sections[1:], 1):
            updated_sections.append("## " + section)
            
            # Add CTA every 2-3 sections
            if i % 2 == 0 and i < len(sections) - 1:
                tool = relevant_tools[min(i // 2 - 1, len(relevant_tools) - 1)]
                cta_block = self._generate_cta_block(tool)
                updated_sections.append(cta_block)
        
        return "\n".join(updated_sections)
    
    def _generate_cta_block(self, tool_data: Dict[str, Any]) -> str:
        """Generate a call-to-action block for a tool."""
        tool_name = tool_data['name']
        description = tool_data['description']
        pricing = tool_data['pricing']
        affiliate_url = tool_data['affiliate_url']
        
        # Get random CTA variation
        cta_variations = tool_data.get('cta_variations', [])
        if not cta_variations:
            cta_variations = self.affiliate_data.get('default_ctas', [])
        
        if cta_variations:
            cta_text = random.choice(cta_variations)
            if '{tool_name}' in cta_text:
                cta_text = cta_text.format(tool_name=tool_name)
        else:
            cta_text = f"Try {tool_name} free"
        
        # Create CTA block
        cta_block = f"""
<div class="affiliate-cta">
<h4>💡 Recommended Tool: {tool_name}</h4>
<p>{description}</p>
<p><strong>Pricing:</strong> {pricing}</p>
<p><a href="{affiliate_url}" target="_blank" rel="noopener">{cta_text} →</a></p>
</div>
"""
        
        return cta_block
    
    def _get_relevant_tools(self, category: str) -> List[Dict[str, Any]]:
        """Get tools relevant to a specific category."""
        relevant_tools = []
        
        for tool_key, tool_data in self.affiliate_data.items():
            if tool_key == 'default_ctas':
                continue
            
            tool_category = tool_data.get('category', '').lower()
            
            # Direct category match
            if category.lower().replace('_', ' ') in tool_category:
                relevant_tools.append(tool_data)
            # Partial match
            elif any(word in tool_category for word in category.lower().split('_')):
                relevant_tools.append(tool_data)
        
        # If no category matches, return popular tools
        if not relevant_tools:
            popular_tools = ['hubspot', 'convertkit', 'asana', 'canva', 'zapier']
            for tool_key in popular_tools:
                if tool_key in self.affiliate_data:
                    relevant_tools.append(self.affiliate_data[tool_key])
        
        return relevant_tools
    
    def _count_affiliate_links(self, content: str) -> int:
        """Count the number of affiliate links in content."""
        # Count markdown links
        markdown_links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))
        
        # Count HTML links in CTA blocks
        html_links = len(re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>', content))
        
        return markdown_links + html_links
    
    def _validate_link_density(self, content: str) -> bool:
        """Validate that affiliate link density is within acceptable range."""
        word_count = len(content.split())
        link_count = self._count_affiliate_links(content)
        
        if word_count == 0:
            return True
        
        density = link_count / word_count
        max_density = self.link_density * 2  # Allow up to 2x the target density
        
        return density <= max_density
    
    def optimize_link_placement(self, content: str) -> str:
        """Optimize the placement of affiliate links for better user experience."""
        # Ensure links are not too close together
        lines = content.split('\n')
        optimized_lines = []
        last_link_line = -10  # Initialize to allow first link
        
        for i, line in enumerate(lines):
            # Check if line contains affiliate link
            if ('<a href=' in line and 'affiliate-cta' in line) or ('[' in line and '](' in line):
                # Ensure minimum distance between links
                if i - last_link_line >= 5:  # At least 5 lines apart
                    optimized_lines.append(line)
                    last_link_line = i
                else:
                    # Skip this link or move it
                    continue
            else:
                optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def generate_link_report(self, content: str) -> Dict[str, Any]:
        """Generate a report on affiliate link performance potential."""
        word_count = len(content.split())
        link_count = self._count_affiliate_links(content)
        density = link_count / word_count if word_count > 0 else 0
        
        # Extract tools mentioned
        mentioned_tools = self._find_mentioned_tools(content)
        
        report = {
            'word_count': word_count,
            'affiliate_links_count': link_count,
            'link_density': density,
            'target_density': self.link_density,
            'density_status': 'optimal' if abs(density - self.link_density) < 0.01 else 'needs_adjustment',
            'mentioned_tools': [tool['data']['name'] for tool in mentioned_tools],
            'recommendations': []
        }
        
        # Add recommendations
        if density < self.link_density * 0.5:
            report['recommendations'].append("Consider adding more affiliate links")
        elif density > self.link_density * 2:
            report['recommendations'].append("Consider reducing affiliate link density")
        
        if len(mentioned_tools) < 2:
            report['recommendations'].append("Consider mentioning more relevant tools")
        
        return report
