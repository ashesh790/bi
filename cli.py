from django.core.management.base import BaseCommand
from user_1.models import User_other_utils


class Command(BaseCommand):
    help = "Remove user_mobile key from user_other_data_json for all instances"

    def handle(self, *args, **kwargs):
        # Get all instances of User_other_utils
        all_instances = User_other_utils.objects.all()

        for instance in all_instances:
            # Check if user_mobile key exists in user_other_data_json
            if "user_mobile" in instance.user_other_data_json:
                instance.user_mobile = instance.user_other_data_json["user_mobile"]
                # Remove user_mobile key
                del instance.user_other_data_json["user_mobile"]
                # Save the instance
                instance.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully removed user_mobile key from user_other_data_json for all instances"
            )
        )
