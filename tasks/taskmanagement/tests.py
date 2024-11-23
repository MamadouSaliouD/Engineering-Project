from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Task, AssignmentGroup

class TaskModelTest(TestCase):
    def setUp(self):
        # Create a user with both email and password
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",  # Ensure email is provided
            password="password123"
        )
        
        # Creating an AssignmentGroup for testing
        self.group = AssignmentGroup.objects.create(name="Test Group")

    def test_task_token_generation_on_create(self):
        # Create a task without specifying task_token
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            assignment_group=self.group,
            creator=self.user,
        )
        self.assertTrue(task.task_token.startswith('TS'))
        self.assertEqual(len(task.task_token), 8)  # Format should be TSXXXXXX

    def test_task_token_increments(self):
        # Create two tasks and check that task_token increments correctly
        task1 = Task.objects.create(
            title="First Task",
            description="This is the first task.",
            assignment_group=self.group,
            creator=self.user,
        )
        task2 = Task.objects.create(
            title="Second Task",
            description="This is the second task.",
            assignment_group=self.group,
            creator=self.user,
        )
        self.assertEqual(int(task2.task_token[2:]), int(task1.task_token[2:]) + 1)

    def test_default_priority(self):
        # Create a task and check that the priority is set to default "P3"
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            assignment_group=self.group,
            creator=self.user,
        )
        self.assertEqual(task.priority, 'P3')

    def test_default_status(self):
        # Create a task and check that the status is set to default "New"
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            assignment_group=self.group,
            creator=self.user,
        )
        self.assertEqual(task.status, 'New')

    def test_task_assignment_group_relationship(self):
        # Check that the task is related to the AssignmentGroup
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            assignment_group=self.group,
            creator=self.user,
        )
        self.assertEqual(task.assignment_group, self.group)

    def test_task_creator_relationship(self):
        # Check that the task is related to the creator (user)
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            assignment_group=self.group,
            creator=self.user,
        )
        self.assertEqual(task.creator, self.user)
