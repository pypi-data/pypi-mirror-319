import logging

from users.models import Group

LOG = logging.getLogger(__name__)


def debug_social(backend, user, response, *args, **kwargs):
    print(f"Backend: {backend}")
    print(f"User: {user}")
    print(f"Response: {response}")


def assign_roles(backend, user, response, *args, **kwargs):
    if not user:
        LOG.error("No user given")
    roles_from_token = response["roles"] if "roles" in response else []
    if not roles_from_token:
        LOG.warning("No roles in response")
    if "NetboxAdmin" in roles_from_token:
        user.is_superuser = True
        roles_from_token.remove("NetboxAdmin")
    else:
        user.is_superuser = False

    groups = Group.objects.filter(name__in=roles_from_token)
    LOG.debug("User %s was added to the following groups: %s", user, groups)
    user.groups.set(groups)
    user.save()


def get_username(strategy, details, backend, user=None, *args, **kwargs):
    storage = strategy.storage
    if not user:
        family_name = details["last_name"].lower()
        given_name = details["first_name"].lower()
        final_username = short_username = f"{given_name[:1]}.{family_name}"

        # Generate a unique username for current user using short_username
        count = 1
        while not final_username or storage.user.user_exists(username=final_username):
            final_username = f"{short_username}.{count}"
            count += 1
    else:
        final_username = storage.user.get_username(user)
    return {"username": final_username}
