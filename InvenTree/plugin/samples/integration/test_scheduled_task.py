""" Unit tests for scheduled tasks"""

from django.test import TestCase

from plugin import registry
from plugin.registry import call_function


class ExampleScheduledTaskPluginTests(TestCase):
    """ Tests for provided ScheduledTaskPlugin """

    def test_function(self):
        """check if the scheduling works"""
        # The plugin should be defined
        self.assertIn('schedule', registry.plugins)
        plg = registry.plugins['schedule']
        self.assertTrue(plg)

        # check that the built-in function is running
        self.assertEqual(plg.member_func(), False)

        # check that the tasks are defined
        self.assertEqual(plg.get_task_names(), ['plugin.schedule.member', 'plugin.schedule.hello', 'plugin.schedule.world'])

        # register
        plg.register_tasks()
        # check that schedule was registers
        from django_q.models import Schedule
        scheduled_plugin_tasks = Schedule.objects.filter(name__istartswith="plugin.")
        self.assertEqual(len(scheduled_plugin_tasks), 3)

        # delete middle task
        # this is to check the system also deals with disappearing tasks
        scheduled_plugin_tasks[1].delete()
        self.assertEqual(len(scheduled_plugin_tasks), 2)

        # test unregistering
        plg.unregister_tasks()
        scheduled_plugin_tasks = Schedule.objects.filter(name__istartswith="plugin.")
        self.assertEqual(len(scheduled_plugin_tasks), 0)

    def test_calling(self):
        """check if a function can be called without errors"""
        self.assertEqual(call_function('schedule', 'member_func'), False)
