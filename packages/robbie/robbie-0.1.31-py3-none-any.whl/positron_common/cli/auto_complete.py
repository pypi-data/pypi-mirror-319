import typer
from positron_common.cli.interactive import (
    FundingSources,
    Environments,
    Images,
)
from positron_common.utils import is_valid_uuid

from rich.console import Console
err_console = Console(stderr=True)   
 # err_console.print(f"ctx.params={ctx.params}") 

"""
Auto complete functions for the `robbie run` command

These implement Typer specific autocompletion logic

https://typer.tiangolo.com/tutorial/options-autocompletion/#access-other-cli-parameters-with-the-context

"""

def funding_group_auto_complete(ctx: typer.Context):
    """
    Funding groups for the CLI autocomplete
    """
    # check if `--environment_id` was already specified
    env = ctx.params.get('environment_arg')
    if (env):
        err_console.print(f"Error: please specify --funding-group first")
        return []
    try:
        fs = FundingSources.load()
        if fs == None:
            return []
        else:
            return fs.auto_complete_items()
    except Exception as e:
        err_console.print(f"[bold red]Auto complete error: {e}") 
        return [" "]
    
def environment_auto_complete(ctx: typer.Context):
    """
    Environments for the CLI autocomplete
    """
    fga = ctx.params.get('funding_arg')
    if (fga):
        # --funding_arg was previously specified
        try:
            envs = Environments.load(fga)
            if envs == None:
                err_console.print(f"Error: There are no environments in group: {fga}.")
                return []
            else:
                return envs.auto_complete_items()
        except Exception as e:
            err_console.print(f"[bold red]Auto complete error: {e}") 
            return [" "]
    else:
        # get the default FG
        try:
            fs = FundingSources.load()
            if fs == None:
                err_console.print(f"Error: Your are not a member of a Group")
                return []
            else:
                envs = Environments.load(fs.default_funding_source_id())
                if envs == None:
                    err_console.print(f"Error: Your have no enviroments in your Personal group.")
                    return []
                else:
                    return envs.auto_complete_items()
        except Exception as e:
            err_console.print(f"[bold red]Auto complete error: {e}") 
        return [" "]
    
    
def images_auto_complete(ctx: typer.Context):
    """
    Images for the CLI autocomplete
    """
    env = ctx.params.get('environment_arg')
    fg = ctx.params.get('funding_arg')
    if fg and env:
        try:
            images = Images.load(fg, env)
            if images == None:
                err_console.print(f"Error: No images are available.")
                return []
            else:
                img_list = images.auto_complete_items()
                img_list.append("auto-select")
                return img_list
        except Exception as e:
            err_console.print(f"[bold red]Auto complete error: {e}") 
        return [" "]
    
    
def set_env_auto_complete():
    return ["local", "dev", "alpha", "beta"]


def jobs_auto_complete(incomplete: str):
    from positron_cli.download import Jobs
    try:
        jobs = Jobs.load()
        if (jobs):
            completion = []
            # returns list of tuples (name, id)
            for name in jobs.auto_complete_items():
                if name[0].startswith(incomplete):
                    completion.append(name)
            return completion
    except Exception as e:
        err_console.print(f"[bold red]Auto complete error: {e}") 
        return [" "]

    