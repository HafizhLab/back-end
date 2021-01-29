from channels.layers import get_channel_layer
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from hafizhlab.challenges.models import Challenge
from hafizhlab.games.models import GameSession


class GameConfigSerializer(serializers.ModelSerializer):
    scope_ct = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())

    class Meta:
        model = Challenge
        fields = [
            'mode',
            'scope_ct',
            'scope_id',
        ]


class GameSessionSerializer(serializers.ModelSerializer):
    # TODO: currently unable to test using in memory backend
    # players_count = serializers.SerializerMethodField()
    challenge_id = serializers.PrimaryKeyRelatedField(
        queryset=Challenge.objects.all(),
        source='challenge',
        write_only=True,
        required=False,
    )
    config = GameConfigSerializer(source='challenge', required=False)

    class Meta:
        model = GameSession
        fields = [
            'room_id',
            'public_code',
            'admin',
            # 'players_count',
            'mode',
            'challenge_id',
            'config',
        ]
        read_only_fields = ['room_id', 'public_code', 'players_count']
        extra_kwargs = {
            'mode': {'write_only': True},
            'admin': {'write_only': True, 'required': False},
        }

    def create(self, validated_data):
        if not isinstance(validated_data['challenge'], Challenge):
            validated_data['challenge'] = Challenge.objects.create(
                    **validated_data['challenge']
            )

        return GameSession.objects.create(**validated_data)

    def get_players_count(self, obj):
        return get_channel_layer().group['game_{}'.format(obj.room_id)]
