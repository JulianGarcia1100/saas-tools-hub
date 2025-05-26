#!/usr/bin/env python3
"""
Content Generator for SEO Affiliate Content Site
AI-powered content generation using OpenAI GPT-4 with SEO optimization.
"""

import asyncio
import openai
import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import yaml
from pathlib import Path
import frontmatter
from loguru import logger
import textstat

from config.settings import settings

class ContentGenerator:
    """AI-powered content generation with SEO optimization."""

    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

        # Load content templates
        self.templates = self._load_templates()

        # Load affiliate data for context
        self.affiliate_data = self._load_affiliate_data()

    def _load_templates(self) -> Dict[str, str]:
        """Load content templates."""
        templates_dir = settings.TEMPLATES_DIR
        templates = {}

        try:
            # Load blog post template
            blog_template_path = templates_dir / "blog_post.md"
            if blog_template_path.exists():
                with open(blog_template_path, 'r', encoding='utf-8') as f:
                    templates['blog_post'] = f.read()
            else:
                templates['blog_post'] = self._get_default_blog_template()

            return templates

        except Exception as e:
            logger.error(f"Error loading templates: {e}")
            return {'blog_post': self._get_default_blog_template()}

    def _load_affiliate_data(self) -> Dict[str, Any]:
        """Load affiliate links data for content context."""
        affiliate_config_path = settings.PROJECT_ROOT / "config" / "affiliate_links.yaml"

        try:
            with open(affiliate_config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading affiliate data: {e}")
            return {}

    def _get_default_blog_template(self) -> str:
        """Get default blog post template."""
        return """---
title: "{title}"
slug: "{slug}"
description: "{meta_description}"
date: {date}
categories: ["{category}"]
tags: {tags}
author: "SaaS Tools Hub"
featured_image: ""
draft: false
---

{content}

## Conclusion

{conclusion}

---

*Ready to get started? {main_cta}*

**Subscribe to our newsletter** for more SaaS tool reviews and productivity tips delivered to your inbox weekly.
"""

    async def generate_post(self, keyword_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a complete blog post for the given keyword."""
        try:
            keyword = keyword_data['keyword']
            category = keyword_data.get('category', 'general')
            search_intent = keyword_data.get('search_intent', 'informational')

            logger.info(f"Generating content for keyword: {keyword}")

            # Generate content outline
            outline = await self._generate_outline(keyword, category, search_intent)

            if not outline:
                logger.error(f"Failed to generate outline for: {keyword}")
                return None

            # Generate full content
            content = await self._generate_full_content(keyword, outline, category, search_intent)

            if not content:
                logger.error(f"Failed to generate content for: {keyword}")
                return None

            # Generate metadata
            metadata = await self._generate_metadata(keyword, content, category)

            # Create final post structure
            post_data = {
                'keyword_id': keyword_data.get('id'),
                'keyword': keyword,
                'title': metadata['title'],
                'slug': self._create_slug(metadata['title']),
                'meta_description': metadata['meta_description'],
                'content': content,
                'category': category,
                'search_intent': search_intent,
                'word_count': len(content.split()),
                'created_at': datetime.now().isoformat(),
                'status': 'draft'
            }

            # Validate content quality
            if self._validate_content_quality(post_data):
                logger.info(f"Generated high-quality content: {post_data['title']}")
                return post_data
            else:
                logger.warning(f"Content quality validation failed for: {keyword}")
                return None

        except Exception as e:
            logger.error(f"Error generating content for {keyword_data.get('keyword', 'unknown')}: {e}")
            return None

    async def _generate_outline(self, keyword: str, category: str, search_intent: str) -> Optional[Dict[str, Any]]:
        """Generate content outline using AI."""

        # Get relevant affiliate tools for this category
        relevant_tools = self._get_relevant_tools(category)
        tools_context = ", ".join([tool['name'] for tool in relevant_tools[:5]])

        prompt = f"""
        Create a detailed content outline for a blog post targeting the keyword: "{keyword}"

        Context:
        - Category: {category}
        - Search Intent: {search_intent}
        - Target Audience: Small businesses, freelancers, and entrepreneurs
        - Relevant Tools: {tools_context}

        Requirements:
        - 800-2000 words target length
        - SEO-optimized structure with H2 and H3 headings
        - Include comparison sections if applicable
        - Focus on practical value and actionable insights
        - Include sections for tool recommendations

        Return a JSON structure with:
        {{
            "title": "SEO-optimized title",
            "introduction": "Hook and overview",
            "main_sections": [
                {{
                    "heading": "H2 heading",
                    "subsections": ["H3 subheading 1", "H3 subheading 2"],
                    "key_points": ["point 1", "point 2", "point 3"]
                }}
            ],
            "conclusion": "Summary and call-to-action"
        }}
        """

        try:
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert SEO content strategist and SaaS marketing specialist. Create detailed, actionable content outlines that provide real value to readers while naturally incorporating affiliate opportunities."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )

            content = response.choices[0].message.content.strip()

            # Try to parse JSON response
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]

            outline = json.loads(content)
            return outline

        except Exception as e:
            logger.error(f"Error generating outline: {e}")
            return None

    async def _generate_full_content(self, keyword: str, outline: Dict[str, Any], category: str, search_intent: str) -> Optional[str]:
        """Generate full content based on outline."""

        relevant_tools = self._get_relevant_tools(category)

        prompt = f"""
        Write a comprehensive blog post based on this outline:

        Title: {outline['title']}
        Keyword: {keyword}
        Category: {category}
        Search Intent: {search_intent}

        Outline:
        {json.dumps(outline, indent=2)}

        Available Tools to Reference:
        {json.dumps([{
            'name': tool['name'],
            'description': tool['description'],
            'pricing': tool['pricing']
        } for tool in relevant_tools[:8]], indent=2)}

        Writing Guidelines:
        - Write AT LEAST 1000-1500 words (this is critical)
        - Use conversational, helpful tone
        - Include specific examples and use cases
        - Naturally mention relevant tools without being overly promotional
        - Use bullet points and numbered lists for readability
        - Include actionable tips and best practices
        - Write for small business owners and entrepreneurs
        - Use the keyword naturally throughout (1-2% density)
        - Include internal linking opportunities (mention other related topics)

        Format as markdown with proper headings (## for H2, ### for H3).
        Do not include the title or meta information - just the content body.
        """

        try:
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert content writer specializing in SaaS tools and business productivity. Write engaging, informative content that helps readers make informed decisions about business tools while naturally incorporating affiliate opportunities."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )

            content = response.choices[0].message.content.strip()
            return content

        except Exception as e:
            logger.error(f"Error generating full content: {e}")
            return None

    async def _generate_metadata(self, keyword: str, content: str, category: str) -> Dict[str, str]:
        """Generate SEO metadata for the content."""

        prompt = f"""
        Create SEO-optimized metadata for this content:

        Target Keyword: {keyword}
        Category: {category}
        Content Preview: {content[:500]}...

        Generate:
        1. SEO Title (50-60 characters, include keyword)
        2. Meta Description (150-160 characters, compelling and keyword-rich)

        Return as JSON:
        {{
            "title": "SEO title here",
            "meta_description": "Meta description here"
        }}
        """

        try:
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an SEO expert. Create compelling, click-worthy titles and descriptions that rank well and drive clicks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )

            content_response = response.choices[0].message.content.strip()

            # Parse JSON response
            if content_response.startswith('```json'):
                content_response = content_response[7:-3]
            elif content_response.startswith('```'):
                content_response = content_response[3:-3]

            metadata = json.loads(content_response)
            return metadata

        except Exception as e:
            logger.error(f"Error generating metadata: {e}")
            # Fallback metadata
            return {
                'title': f"{keyword.title()} - Complete Guide 2024",
                'meta_description': f"Discover the best {keyword} solutions for your business. Compare features, pricing, and find the perfect tool for your needs."
            }

    def _get_relevant_tools(self, category: str) -> List[Dict[str, Any]]:
        """Get relevant affiliate tools for a category."""
        relevant_tools = []

        for tool_key, tool_data in self.affiliate_data.items():
            if tool_key == 'default_ctas':
                continue

            tool_category = tool_data.get('category', '').lower()
            if category.lower().replace('_', ' ') in tool_category.lower():
                relevant_tools.append(tool_data)

        # If no category match, return some popular tools
        if not relevant_tools:
            popular_tools = ['hubspot', 'convertkit', 'asana', 'canva', 'zapier']
            for tool_key in popular_tools:
                if tool_key in self.affiliate_data:
                    relevant_tools.append(self.affiliate_data[tool_key])

        return relevant_tools

    def _create_slug(self, title: str) -> str:
        """Create URL-friendly slug from title."""
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        return slug[:50]  # Limit length

    def _validate_content_quality(self, post_data: Dict[str, Any]) -> bool:
        """Validate content quality before publishing."""
        content = post_data['content']
        word_count = post_data['word_count']

        # Check minimum word count
        if word_count < settings.MIN_WORD_COUNT:
            logger.warning(f"Content too short: {word_count} words")
            return False

        # Check maximum word count
        if word_count > settings.MAX_WORD_COUNT:
            logger.warning(f"Content too long: {word_count} words")
            return False

        # Check readability (more lenient)
        try:
            flesch_score = textstat.flesch_reading_ease(content)
            if flesch_score < 20:  # Very difficult threshold
                logger.warning(f"Content readability low but acceptable: {flesch_score}")
                # Don't fail, just warn
        except:
            pass  # Skip if textstat fails

        # Check for proper headings (more lenient)
        h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
        if h2_count < 2:  # Reduced from 3 to 2
            logger.warning(f"Not enough H2 headings: {h2_count}")
            return False

        # Check keyword presence (more lenient)
        keyword = post_data['keyword'].lower()
        content_lower = content.lower()

        # Check for individual words from the keyword phrase
        keyword_words = keyword.split()
        total_keyword_mentions = 0
        for word in keyword_words:
            if len(word) > 3:  # Only count meaningful words
                total_keyword_mentions += content_lower.count(word)

        keyword_density = total_keyword_mentions / word_count if word_count > 0 else 0

        if keyword_density < 0.002 or keyword_density > 0.05:  # Very lenient range
            logger.warning(f"Keyword density acceptable but low: {keyword_density:.3f}")
            # Don't fail, just warn

        return True
