import glob
import pandas as pd

from collections import Counter
from loader import get_messenger_json


class MessageStorage:
    def __init__(self):
        self.path = ""
        self.messages = {}

    def read_messages(self, path: str):
        self.path = path
        self.messages: dict = {}

        for chat_dir in glob.glob(self.path + "/*"):

            chat_title = get_messenger_json(chat_dir + "/message_1.json")["title"]

            messages = []
            for message_file in glob.glob(chat_dir + "/message_*.json"):
                message_data = get_messenger_json(message_file)
                messages.extend(message_data["messages"])

            self.messages[chat_title] = messages

    def get_participants(self, title: str):
        if title in self.messages:
            df = pd.DataFrame(self.messages[title])
            participants = df['sender_name'].unique().tolist()
            return participants
        else:
            return None

    def get_messages_count(self):
        counts: dict = {}
        for title, messages in self.messages.items():
            count = len(messages)
            counts[title] = count

        return {k: v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}

    def get_titles(self):
        counts = {title: len(messages) for title, messages in self.messages.items()}
        sorted_titles = [k for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)]
        return sorted_titles

    def get_participant_count(self, title: str):
        if title not in self.messages:
            return {}

        participant_counts = Counter(message["sender_name"] for message in self.messages[title])
        return participant_counts

    def get_messages_by_time(self, title: str, daily_interval: int = 1):
        if title in self.messages:
            df = pd.DataFrame(self.messages[title])

            df['datetime'] = pd.to_datetime(df['timestamp_ms'], unit='ms')

            messages_by_time = df.groupby(pd.Grouper(key='datetime', freq=f'{daily_interval}D')).size().reset_index(
                name='message_count')

            return messages_by_time.set_index("datetime")
        else:
            return None

    def get_messages_by_time_by_sender(self, title: str, daily_interval: int = 7):
        if title in self.messages:
            df = pd.DataFrame(self.messages[title])

            df['datetime'] = pd.to_datetime(df['timestamp_ms'], unit='ms')

            messages_by_time = df.groupby(
                ['sender_name', pd.Grouper(key='datetime', freq=f'{daily_interval}D')]).size().reset_index(
                name='message_count')

            return messages_by_time
        else:
            return None

    def get_all_reactions(self, title: str):
        if title in self.messages:
            df = pd.DataFrame(self.messages[title])
            all_reactions = []

            for _, message in df.iterrows():
                if "reactions" in message and isinstance(message['reactions'], list):
                    reactions = [reaction['reaction'] for reaction in message['reactions']]
                    all_reactions.extend(reactions)

            reaction_counts = Counter(all_reactions)
            sorted_reactions = [f"{k} ({v})" for k, v in sorted(reaction_counts.items(), key=lambda item: item[1], reverse=True)]

            return sorted_reactions
        else:
            return None

    def get_reaction_matrix(self, title: str, reaction: list = None):
        if title in self.messages:
            df = pd.DataFrame(self.messages[title])
            participants = df['sender_name'].unique()
            matrix = pd.DataFrame(index=participants, columns=participants, data=0)

            for _, message in df.iterrows():
                if "reactions" in message and isinstance(message['reactions'], list):
                    for reaction_info in message['reactions']:
                        actor = reaction_info['actor']
                        reacted = reaction_info['reaction']

                        if reaction is None or reacted in reaction:
                            matrix.loc[actor, message['sender_name']] += 1

            for participant in participants:
                matrix[participant] = matrix[participant] / df[df['sender_name'] == participant].shape[0]

            return matrix
        else:
            return None

    def get_reaction_counts_by_participant(self, title: str, top_n: int = 4):
        if title in self.messages:
            df = pd.DataFrame(self.messages[title])
            reaction_counts_for_participant = {}

            for _, message in df.iterrows():
                if "reactions" in message and isinstance(message['reactions'], list):
                    for reaction_info in message['reactions']:
                        reacted = reaction_info['reaction']

                        sender_name = message['sender_name']

                        if sender_name not in reaction_counts_for_participant:
                            reaction_counts_for_participant[sender_name] = {}

                        if reacted not in reaction_counts_for_participant[sender_name]:
                            reaction_counts_for_participant[sender_name][reacted] = 0

                        reaction_counts_for_participant[sender_name][reacted] += 1

            sorted_counts = {
                participant: {reacted: count for reacted, count in
                              sorted(reactions.items(), key=lambda x: x[1], reverse=True)[:top_n]}
                for participant, reactions in reaction_counts_for_participant.items()
            }

            return sorted_counts
        else:
            return None

