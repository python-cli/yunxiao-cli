## yunxiao-cli

This CLI tool is used to check the yunxiao projects' workitems.



#### Preview

```bash
➜  yunxiao-cli
Usage: yunxiao-cli [OPTIONS] COMMAND [ARGS]...

  CLI tool for managing yunxiao projects

Options:
  --help  Show this message and exit.

Commands:
  do            Do something magic.
  organization  Project management commands
  project       Project management commands
  workitem      Workitem management commands
```

Check the organization list:

```bash
➜  yunxiao-cli organization --help
Usage: yunxiao-cli organization [OPTIONS] COMMAND [ARGS]...

  Project management commands

Options:
  --help  Show this message and exit.

Commands:
  list  List all the organizations
```

Check the project list:

```bash
➜  yunxiao-cli project --help
Usage: yunxiao-cli project [OPTIONS] COMMAND [ARGS]...

  Project management commands

Options:
  --help  Show this message and exit.

Commands:
  all     List/Reload the builtin and following projects
  field   List all the projects' field
  info    Get workitem details
  list    List the cached projects
  member  List all members under the project
  status  List the project's statuses
```

Check the workitems:

```bash
➜  yunxiao-cli workitem --help
Usage: yunxiao-cli workitem [OPTIONS] COMMAND [ARGS]...

  Workitem management commands

Options:
  --help  Show this message and exit.

Commands:
  bug   List bug workitems with filters
  info  Get workitems details
  task  List task workitems with filters
```

Check the workitems by category:

```
➜  yunxiao-cli workitem task --help
Usage: yunxiao-cli workitem task [OPTIONS]

  List task workitems with filters

Options:
  --assigned-to TEXT      User ID/Name
  --statuses TEXT         Workitem statuses, use comma as separator
  --not-in-statuses TEXT  Reversed workitem statuses, use comma as separator
  --help                  Show this message and exit.
```



#### Configuration

After running an initial command, a default configuration file will be generated at `~/.config/yunxiao-cli/config.yaml`, edit the file directly and fill the required fields:

```yaml
# User Credential
# https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair
CREDENTIAL:
    access_key_id: 
    access_key_secret: 
    
    # Open page https://myaccount.console.aliyun.com/overview and copy the value of "账号ID"
    aliyun_account_id: 

TEAM:
    endpoint: devops.cn-hangzhou.aliyuncs.com
    organization: 
```

**Fields**:

* `access_key_id` and `access_key_secret`: the key of aliyun to access all the platform data.

* `aliyun_account_id`: the unique identifier of user.

* `endpoint`: a default endpoint sent to aliyun, don't edit the default value if necessary.

* `organization`: if you have multiple organizations under the account, feel free to specifiy an explicit identifier.

  > You could get the organization identifier by running `yunxiao-cli organization [list]`.



**Important Notes**:

All the projects' data including fields, statuses, members will be cached to the local system under the directory `~/.config/yunxiao-cli/cache.yaml`, it's your duty to update the meta data in a period of time, *especially after the organization's administrator updated the project/field/status list*. Here is the command:

```bash
yunxiao-cli project all --reload
```

If the organization use the project set features, use the following command:

```bash
yunxiao-cli project all --reload --reload-project-set
```

> Aliyun doesn't have open api to access the project sets, so it will request you to access the data via chome.



#### Custom Commands

Every project has its own custom work item fields which are not standard, so here is the plugin system. You could inject any custom command after the `yunxiao-cli do`  command.

Add your custom commands in config file `~/.config/yunxiao-cli/config.yaml`:

```yaml

COMMAND:
    - /path/to/reminder.py
```

Here is an example of `reminder.py`:

```python
import click 
import subprocess
from datetime import datetime, timedelta

from yunxiao.utils.state import *
from yunxiao.utils.date import *
from yunxiao.utils.output import *
from yunxiao.sdk.category import *
from yunxiao.model.workitem import *

def show_notification(title, message):
    subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'])

def show_dialog(title, message, buttons=None, default_button=""):
    script = f'''
    display dialog "{message}" with title "{title}" '''

    script += f'buttons "Got it" '
    script += 'with icon note'

    subprocess.run(['osascript', '-e', script])


class Command:

    @classmethod
    def name(cls) -> str:
        return 'reminder'

    @classmethod
    def help(cls) -> str:
        return 'Remind me the due workitems.'
    
    @classmethod
    def arguments(cls) -> List[click.Parameter]:
        return []
    
    @classmethod
    def options(cls) -> List[click.Parameter]:
        return [
            click.Option(['--raw'], is_flag=True, default=False, help='Show raw output instead of system dialog'),
        ]

    def run(self, **kwargs):
        raw_format = kwargs.get('raw')
        org = GlobalState.current().organization_id
        content = ''
        tomorrow = (datetime.now() + timedelta(days=1)).date()

        def get_due_workitems(workitems) -> List[WorkItem]:
            results: List[WorkItem] = []
            workitems = list(map(lambda x: WorkItemDetailAPI.run(org, x.identifier), workitems))

            for item in workitems:
                due_field_id = GlobalState.current().get_matching_field_id(project.identifier, Category.Task.value, '计划完成时间')
                due_date_str = item.get_display_value_of_custom_field(due_field_id)

                if due_date_str:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M:%S').date()
                    if due_date <= tomorrow:
                        results.append(item)

            return results

        for project, workitems in list_workitem_by(Category.Task, None, None, '已完成,已取消'):
            workitems = get_due_workitems(workitems)

            if workitems:
                if raw_format:
                    show_table_workitem(workitems)
                else:
                    content += project.name + ':\n'
                    
                    for item in workitems:
                        due_field_id = GlobalState.current().get_matching_field_id(project.identifier, Category.Task.value, '计划完成时间')
                        due_date = item.get_display_value_of_custom_field(due_field_id)
                        content += '\t' + item.serialNumber + ' ⚠️⚠️⚠️\n\t' + item.subject + '\n\t' + item.status + '\n\t逾期时间: ' + due_date + '\n'
                    else:
                        content += '\n'

        for project, workitems in list_workitem_by(Category.Bug, None, None, '已修复,暂不修复,已关闭'):
            workitems = get_due_workitems(workitems)

            if workitems:

                if raw_format:
                    show_table_workitem(workitems)
                else:
                    content += project.name + ':\n'
                    
                    for item in workitems:
                        due_field_id = GlobalState.current().get_matching_field_id(project.identifier, Category.Task.value, '计划完成时间')
                        due_date = item.get_display_value_of_custom_field(due_field_id)
                        content += '\t' + item.serialNumber + ' ⚠️⚠️⚠️\n\t' + item.subject + '\n\t' + item.status + '\n\t逾期时间: ' + due_date + '\n'
                    else:
                        content += '\n'

        content = content.strip()

        if raw_format:
            print(content)
        else:
            if len(content) <= 0:
                content = '🎉🎉🎉 You finished all the work'

            show_dialog('Reminder', content)
```

Now you could run the following command to get a reminder:

```bash
yunxiao-cli do reminder
```

Enjoy!



#### Author

[Will Han](https://github.com/xingheng)



#### License

MIT