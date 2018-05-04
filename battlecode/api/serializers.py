"""
The medium between JSON and Python database objects. Also any
events that need to happen before, during, or after serializing
or deserializing objects.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import *

class LeagueHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, 'pk') and obj.pk is None:
            return None

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}
        kwargs['league_id'] = self.context['league_id']
        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class BasicUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('url', 'username', 'avatar', 'bio', 'country')
        read_only_fields = ('url', 'username', 'avatar', 'bio', 'country')


class FullUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'date_of_birth',
            'username', 'avatar', 'bio', 'country')
        read_only_fields = ('url', 'avatar')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Create and return a new user, given the validated data.
        """
        try:
            return get_user_model().objects.create_user(**validated_data)
        except Exception as e:
            error = {'message': ','.join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)

    def update(self, instance, validated_data):
        """
        Update and return an existing user object, given the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance


class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = League
        fields = '__all__'


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    serializer_url_field = LeagueHyperlinkedIdentityField
    league = serializers.SlugRelatedField(queryset=League.objects.all(), slug_field='id')
    users = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field='username', many=True)

    class Meta:
        model = Team
        fields = ('url', 'id', 'league', 'name', 'avatar', 'users',
            'bio', 'divisions', 'auto_accept_ranked', 'auto_accept_unranked')
        read_only_fields = ('id', 'avatar',)

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.divisions = validated_data.get('divisions', instance.divisions)
        instance.auto_accept_ranked = validated_data.get('auto_accept_ranked', instance.auto_accept_ranked)
        instance.auto_accept_unranked = validated_data.get('auto_accept_unranked', instance.auto_accept_unranked)
        instance.save()
        return instance


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    serializer_url_field = LeagueHyperlinkedIdentityField
    team = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='id')

    class Meta:
        model = Submission
        fields = ('url', 'id', 'team', 'name', 'filename', 'submitted_at')


class MapSerializer(serializers.HyperlinkedModelSerializer):
    serializer_url_field = LeagueHyperlinkedIdentityField
    league = serializers.SlugRelatedField(queryset=League.objects.all(), slug_field='id')

    class Meta:
        model = Map
        fields = ('url', 'id', 'league', 'name', 'filename')


class ScrimmageSerializer(serializers.HyperlinkedModelSerializer):
    serializer_url_field = LeagueHyperlinkedIdentityField
    league          = serializers.SlugRelatedField(queryset=League.objects.all(), slug_field='id')
    map             = serializers.SlugRelatedField(queryset=Map.objects.all(), slug_field='id')
    red_team        = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='id')
    blue_team       = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='id')
    red_submission  = serializers.SlugRelatedField(queryset=Submission.objects.all(), slug_field='id', required=False)
    blue_submission = serializers.SlugRelatedField(queryset=Submission.objects.all(), slug_field='id', required=False)
    requested_by    = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='id')

    class Meta:
        model = Scrimmage
        fields = ('url', 'id', 'league', 'red_team', 'blue_team', 'map', 'ranked',
            'red_submission', 'blue_submission', 'status', 'replay', 'red_logs', 'blue_logs',
            'requested_by', 'requested_at', 'started_at', 'updated_at')
        read_only_fields = ('url', 'replay', 'red_logs', 'blue_logs', 'requested_at', 'started_at', 'updated_at')


class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tournament
        fields = ('url', 'league', 'name', 'style', 'date_time', 'divisions', 'maps', 'stream_link')


class TournamentScrimmageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TournamentScrimmage
