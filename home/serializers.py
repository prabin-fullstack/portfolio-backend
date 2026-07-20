from rest_framework import serializers
from .models import HeroContent, AboutContent, Stat, Messages


class HeroContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroContent
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'


class StatSerializer(serializers.ModelSerializer):
    # id must be optional+writable here so the nested payload can tell us
    # "this is stat #3, update it" vs "this has no id, create it".
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Stat
        # NOTE: "about" is deliberately excluded — it's set automatically
        # in AboutContentSerializer.update(), not sent by the client.
        fields = ["id", "value", "suffix", "label", "order"]


class AboutContentSerializer(serializers.ModelSerializer):
    # was: stats = StatSerializer(many=True, read_only=True)  <-- the bug
    stats = StatSerializer(many=True, required=False)

    class Meta:
        model = AboutContent
        fields = "__all__"

    def update(self, instance, validated_data):
        stats_data = validated_data.pop("stats", None)

        # update the plain About fields (eyebrow, heading, bio, ...)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if stats_data is not None:
            existing = {s.id: s for s in instance.stats.all()}
            keep_ids = set()

            for item in stats_data:
                item_id = item.get("id")
                # item_id is a real DB id -> update that row
                if item_id and item_id in existing:
                    stat = existing[item_id]
                    for key, value in item.items():
                        if key != "id":
                            setattr(stat, key, value)
                    stat.save()
                    keep_ids.add(item_id)
                # no id, or an id we don't recognise (e.g. a client-side
                # temp id) -> this is a new row
                else:
                    item.pop("id", None)
                    stat = Stat.objects.create(about=instance, **item)
                    keep_ids.add(stat.id)

            # anything that existed before but wasn't in the payload
            # was removed on the client -> delete it
            for stat_id, stat in existing.items():
                if stat_id not in keep_ids:
                    stat.delete()

        return instance
    

