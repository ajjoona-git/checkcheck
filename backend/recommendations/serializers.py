from rest_framework import serializers

# 추천 시뮬레이션 미리보기 요청용 시리얼라이저
class RecommendationPreviewSerializer(serializers.Serializer):
    target_amount = serializers.IntegerField(min_value=0)
    start_amount = serializers.IntegerField(min_value=0)
    term_months = serializers.IntegerField(min_value=1, max_value=120)
    purpose = serializers.ChoiceField(choices=["GOAL", "SHORT", "SAFE", "HABIT", "YIELD"])

    top_k = serializers.IntegerField(required=False, default=10, min_value=1, max_value=50)
    per_product_candidates = serializers.IntegerField(required=False, default=3, min_value=1, max_value=7)

    def validate(self, attrs):
        return attrs