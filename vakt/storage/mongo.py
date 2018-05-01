"""
MongoDB storage for Policies.
"""

import logging

from ..storage.abc import Storage
from ..exceptions import PolicyExistsError


DEFAULT_COLLECTION = 'vakt'

log = logging.getLogger(__name__)


class MongoStorage(Storage):
    """Stores all policies in MongoDB"""

    def __init__(self, client, collection=DEFAULT_COLLECTION):
        self.client = client
        self.db = self.client[collection]

    def add(self, policy):
        uid = policy.uid
        try:
            self.db.insert_one(policy.to_json())
        except Exception:
            log.error('Error trying to create already existing policy with UID=%s', uid)
            raise PolicyExistsError

    def get(self, uid):
        return self.policies.get(uid)

    def get_all(self, limit, offset):
        result = [v for v in self.policies.values()]
        if limit + offset > len(result):
            limit = len(result)
            offset = 0
        return result[offset:limit + offset]

    def find_for_inquiry(self, inquiry):
        with self.lock:
            return list(self.policies.values())

    def update(self, policy):
        self.policies[policy.uid] = policy

    def delete(self, uid):
        if uid in self.policies:
            del self.policies[uid]