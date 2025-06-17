# Behavioral Design Patterns
# Focus on how objects interact with each other and how they communicate to acompolish tasks.

# State Pattern:
# Allows an object to behave differently depending on the state it is in

# Writing a blog post using wordpress. The document can be in one of 3 states:
# 1. Draft
# 2. Moderation
# 3. Published

# Three types of user roles:
# 1. Reader
# 2. Editor
# 3. Admin

# Only admins can publish posts
from enum import Enum

class DocumentStates(Enum):
    DRAFT = 1
    MODERATION = 2
    PUBLISHED = 3
    
class UserRoles(Enum):
    READER = 1
    EDITOR = 2
    ADMIN = 3

# class Document:
#     def __init__(self, state: DocumentStates, current_user_role: UserRoles):
#         self.state = state
#         self.current_user_role = current_user_role
#     # This violates the SOLID because publish has to be modified in the user rol or document states updates
#     def publish(self):
#         if self.state == DocumentStates.DRAFT:
#             self.state = DocumentStates.MODERATION
#         elif self.state == DocumentStates.MODERATION and self.current_user_role == UserRoles.ADMIN:
#             self.state = DocumentStates.PUBLISHED
#         elif self.state == DocumentStates.PUBLISHED:
#             pass # Do nothing
    
# doc1 = Document(DocumentStates.DRAFT, UserRoles.EDITOR)
# print(doc1.state)
# doc1.publish()
# print(doc1.state)
# doc1.publish()
# print(doc1.state)

# doc2 = Document(DocumentStates.DRAFT, UserRoles.READER)
# print(doc2.state)
# doc2.publish()
# print(doc2.state)
# doc2.publish()
# print(doc2.state)

# doc3 = Document(DocumentStates.DRAFT, UserRoles.ADMIN)
# print(doc3.state)
# doc3.publish()
# print(doc3.state)
# doc3.publish()
# print(doc3.state)


# Refactored Solution
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def publish(self, document):
        pass

class DraftState(State):
    def __init__(self, document):
        self._document = document
    
    def publish(self):
        self._document.state = ModerationState(self._document)

class ModerationState(State):
    def __init__(self, document):
        self._document = document

    def publish(self):
        if self._document.current_user_role == UserRoles.ADMIN:
            self._document.state = PublishedState(self._document)

class PublishedState(State):
    def __init__(self, document):
        self._document = document

    def publish(self):
        pass
        
# This document delegates the behavior to state specific classes
class Document:
    def __init__(self, current_user_role: UserRoles):
        self.state = DraftState(self) #Initialize state as draft state when creating a document class
        self.current_user_role = current_user_role


    def publish(self):
        self.state.publish()

doc = Document(UserRoles.ADMIN)
print(doc.state.__class__.__name__)

doc.publish()
print(doc.state.__class__.__name__)

doc.publish()
print(doc.state.__class__.__name__)

# Using state pattern can be over-engineering. f
        


        
        