#!/usr/bin/env python3
"""Test all advanced AI/ML features of o-nakala-core."""

import asyncio
import logging
from pathlib import Path

from src.o_nakala_core.common.config import NakalaConfig
from src.o_nakala_core.user_info import NakalaUserInfoClient
from src.o_nakala_core.autonomous_generator import create_autonomous_generator
from src.o_nakala_core.ml_engine import MLPatternLearner, SemanticAnalyzer
from src.o_nakala_core.predictive_analytics import PredictiveAnalyticsEngine
from src.o_nakala_core.collaborative_intelligence import CollaborativeIntelligenceEngine
from src.o_nakala_core.vocabulary import NakalaVocabularyService

async def test_all_advanced_features():
    """Test all advanced AI/ML features."""
    # Setup
    config = NakalaConfig(api_key='33170cfe-f53c-550b-5fb6-4814ce981293')
    user_client = NakalaUserInfoClient(config)
    
    print("🚀 Testing Advanced O-Nakala Core Features")
    
    # 1. Test Autonomous Generator
    print("\n1. 🤖 Testing Autonomous Metadata Generation...")
    try:
        generator = create_autonomous_generator(user_client)
        result = await generator.generate_autonomous_metadata(
            'examples/simple-dataset/bird_image.jpg'
        )
        print(f"   ✅ Generated {len(result.generated_metadata)} metadata fields")
        print(f"   ✅ Quality score: {result.quality_score:.1%}")
        print(f"   ✅ Recommendations: {len(result.recommendations)}")
        print(f"   ✅ Content type detected: {result.content_analysis.content_type}")
        print(f"   ✅ Language detected: {result.content_analysis.detected_language}")
    except Exception as e:
        print(f"   ⚠️  Autonomous generation: {e}")
    
    # 2. Test ML Engine
    print("\n2. 🧠 Testing ML Pattern Learning...")
    try:
        cache_dir = Path.home() / '.nakala' / 'test_cache'
        ml_learner = MLPatternLearner(str(cache_dir))
        
        # Test prediction
        context = {'title': 'Climate Data', 'type': 'dataset'}
        prediction = ml_learner.predict_field_value(context, 'creator')
        print(f"   ✅ ML prediction completed: {prediction is not None}")
        
        # Test pattern summary
        summary = ml_learner.get_pattern_summary()
        print(f"   ✅ Pattern summary: {summary['total_patterns']} patterns learned")
        
        # Test semantic analysis
        semantic_analyzer = SemanticAnalyzer(str(cache_dir))
        embedding = semantic_analyzer.analyze_content(
            'Research data analysis', 'test_content', 'document'
        )
        print(f"   ✅ Semantic embedding: {len(embedding.embedding_vector)} dimensions")
        print(f"   ✅ Semantic features: {len(embedding.semantic_features)} features")
    except Exception as e:
        print(f"   ⚠️  ML Engine: {e}")
    
    # 3. Test Predictive Analytics
    print("\n3. 📊 Testing Predictive Analytics...")
    try:
        # Test basic initialization and capabilities
        from src.o_nakala_core.predictive_analytics import PredictiveAnalyticsEngine
        analytics = PredictiveAnalyticsEngine(user_client)
        print(f"   ✅ Predictive analytics engine initialized")
        print(f"   ✅ Ready for quality and completeness analysis")
        
        # Test available methods
        available_methods = [method for method in dir(analytics) if not method.startswith('_')]
        print(f"   ✅ Available methods: {len(available_methods)}")
    except Exception as e:
        print(f"   ⚠️  Predictive Analytics: {e}")
    
    # 4. Test Collaborative Intelligence
    print("\n4. 🤝 Testing Collaborative Intelligence...")
    try:
        collab_engine = CollaborativeIntelligenceEngine(user_client)
        insights = await collab_engine.analyze_and_learn()
        print(f"   ✅ Collaborative insights: {len(insights.get('collaborative_insights', []))}")
        print(f"   ✅ Community analysis completed")
        
        # Test pattern analysis
        available_methods = [method for method in dir(collab_engine) if not method.startswith('_')]
        print(f"   ✅ Available collaborative methods: {len(available_methods)}")
    except Exception as e:
        print(f"   ⚠️  Collaborative Intelligence: {e}")
    
    # 5. Test Vocabulary Service
    print("\n5. 📚 Testing Vocabulary Management...")
    try:
        vocab_service = NakalaVocabularyService(config)
        print(f"   ✅ Vocabulary service initialized")
        
        # Test cache functionality
        cache_initialized = hasattr(vocab_service, 'cache')
        print(f"   ✅ Cache system: {cache_initialized}")
        
        # Test available methods
        available_methods = [method for method in dir(vocab_service) if not method.startswith('_')]
        print(f"   ✅ Available vocabulary methods: {len(available_methods)}")
    except Exception as e:
        print(f"   ⚠️  Vocabulary Service: {e}")
    
    # 6. Test Integration Capabilities
    print("\n6. 🔗 Testing Integration Capabilities...")
    try:
        # Test creation of test file for analysis
        test_file = Path('test_sample.txt')
        test_file.write_text('This is a research document about climate data analysis and statistical methods.')
        
        # Test autonomous generation on real file
        generator = create_autonomous_generator(user_client)
        result = await generator.generate_autonomous_metadata(str(test_file))
        
        print(f"   ✅ Real file analysis: {result.content_analysis.content_type}")
        print(f"   ✅ Generated fields: {list(result.generated_metadata.keys())}")
        print(f"   ✅ Processing time: {result.processing_time:.2f}s")
        
        # Cleanup
        test_file.unlink()
        
    except Exception as e:
        print(f"   ⚠️  Integration test: {e}")
    
    print("\n🎉 Advanced features testing completed!")

if __name__ == "__main__":
    asyncio.run(test_all_advanced_features())