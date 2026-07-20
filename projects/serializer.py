from rest_framework import serializers
from .models import Project, ProjectSection


class ProjectSerializer(serializers.ModelSerializer):
    tag_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "section",
            "title",
            "year",
            "role",
            "description",
            "tags",
            "tag_list",
            "image",
            "live_url",
            "code_url",
            "order",
        ]
        read_only_fields = ["section"]

    def get_tag_list(self, obj):
        if not obj.tags:
            return []
        return [tag.strip() for tag in obj.tags.split(",")]


class ProjectSectionSerializer(serializers.ModelSerializer):
    """
    Nested read for the public Work section: eyebrow/heading/intro plus
    every project underneath it, already ordered.
    """
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectSection
        fields = ["id", "eyebrow", "heading", "intro", "projects"]