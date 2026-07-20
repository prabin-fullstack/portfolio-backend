from rest_framework import serializers
from .models import SkillsSection, SkillGroup, Skill


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Skill
        fields = "__all__"
        extra_kwargs = {
            "group": {"required": False},
        }


class SkillGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    skills = SkillSerializer(many=True)

    class Meta:
        model = SkillGroup
        fields = "__all__"
        extra_kwargs = {
            "section": {"required": False},
        }


class SkillsSectionSerializer(serializers.ModelSerializer):
    groups = SkillGroupSerializer(many=True)

    class Meta:
        model = SkillsSection
        fields = "__all__"

    def update(self, instance, validated_data):
        groups_data = validated_data.pop("groups", [])

        # Update section
        instance.eyebrow = validated_data.get("eyebrow", instance.eyebrow)
        instance.heading = validated_data.get("heading", instance.heading)
        instance.intro = validated_data.get("intro", instance.intro)
        instance.save()

        # Delete old groups (skills are deleted automatically)
        instance.groups.all().delete()

        # Recreate groups and skills
        for group_data in groups_data:
            skills_data = group_data.pop("skills", [])

            group = SkillGroup.objects.create(
                section=instance,
                title=group_data.get("title", ""),
                note=group_data.get("note", ""),
                order=group_data.get("order", 0),
            )

            for skill_data in skills_data:
                Skill.objects.create(
                    group=group,
                    name=skill_data.get("name", ""),
                    icon=skill_data.get("icon", ""),
                    color=skill_data.get("color", "F5F1EA"),
                    level=skill_data.get("level", Skill.Level.SECONDARY),
                    note=skill_data.get("note", ""),
                    order=skill_data.get("order", 0),
                )

        return instance