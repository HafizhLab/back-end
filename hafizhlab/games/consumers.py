from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.core.exceptions import PermissionDenied

from hafizhlab.games.models import GameSession


class GameConsumer(JsonWebsocketConsumer):
    game_started = False

    def connect(self):
        from pprint import pprint
        pprint(self.scope)
        print(type(self.scope['query_string']))
        self.user = self.scope['user']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'game_{}'.format(self.room_id)

        self.game_session = GameSession.objects.get(room_id=self.room_id)

        if self.game_session.mode == GameSession.Mode.MULTI_PLAYER:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name,
            )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data, **kwargs):
        if text_data == 'game_start':
            if not self.game_started:
                if self.game_session.admin == self.user:
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'game_start',
                        }
                    )
                else:
                    raise PermissionDenied()
            else:
                print('game has been started')
        else:
            super().receive(text_data, **kwargs)

    def receive_json(self, content):
        print(content)

    def game_start(self, event):
        self.game_started = True
