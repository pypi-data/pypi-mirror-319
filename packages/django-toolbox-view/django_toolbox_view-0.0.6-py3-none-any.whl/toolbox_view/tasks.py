import importlib

from ajax_helpers.utils import ajax_command
from celery import shared_task

from toolbox_view.helpers import has_confirm


@shared_task(bind=True)
def toolbox_task(self, config=False, slug=None, **_kwargs):
    if config:
        return {'progress': False, 'message': 'Running ', 'title': 'Please wait....'}
    import_module = importlib.import_module(slug['module'])
    function = getattr(import_module, slug['class_name'])(modal_task=self).button_function
    commands = function(confirm='task') if has_confirm(function) else function()
    if not isinstance(commands, list):
        commands = [ajax_command('close'),
                    ajax_command('message', text='Finished Executing \n\n' + slug['class_name'])]
    else:
        commands.insert(0, ajax_command('close'))
    return {'commands': commands}
