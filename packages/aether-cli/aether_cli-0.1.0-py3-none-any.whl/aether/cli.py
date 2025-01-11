import asyncio
import click
import sys
from halo import Halo
from .config import Config
from .models import get_model_class

def async_command(f):
    """Decorator to run async click commands"""
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """AI CLI tool for chatting with different AI models"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config()
    
    if ctx.invoked_subcommand is None:
        return chat_loop(ctx)

@cli.command()
@click.argument('model')
@click.argument('api_key')
@click.pass_context
def set(ctx, model, api_key):
    """Set API key for a specific model"""
    if ctx.obj is None:
        ctx.ensure_object(dict)
        ctx.obj['config'] = Config()
    
    config = ctx.obj['config']
    config.set_api_key(model, api_key)
    click.echo(f"API key for {model} has been set")

@cli.command()
@click.argument('model')
@click.pass_context
def use(ctx, model):
    """Switch to using a specific model"""
    if ctx.obj is None:
        ctx.ensure_object(dict)
        ctx.obj['config'] = Config()
        
    config = ctx.obj['config']
    if config.get_api_key(model) is None:
        click.echo(f"No API key set for {model}. Please set it first using 'ask set {model} <api_key>'")
        return
    config.set_current_model(model)
    click.echo(f"Switched to {model}")

@cli.command()
@click.argument('proxy_url', required=False)
@click.pass_context
def proxy(ctx, proxy_url):
    """Set or show proxy settings"""
    if ctx.obj is None:
        ctx.ensure_object(dict)
        ctx.obj['config'] = Config()
    
    config = ctx.obj['config']
    
    if proxy_url is None:
        # 显示当前代理设置
        current_proxy = config.get_proxy()
        if current_proxy:
            click.echo(f"Current proxy: {current_proxy}")
        else:
            click.echo("No proxy configured")
    else:
        # 设置新的代理
        if proxy_url.lower() in ['none', 'off', 'disable']:
            config.set_proxy(None)
            click.echo("Proxy disabled")
        else:
            config.set_proxy(proxy_url)
            click.echo(f"Proxy set to: {proxy_url}")

@async_command
async def chat_loop(ctx):
    """Main chat loop"""
    if ctx.obj is None:
        ctx.ensure_object(dict)
        ctx.obj['config'] = Config()
        
    config = ctx.obj['config']
    current_model = config.get_current_model()
    
    if not current_model:
        click.echo("No model selected. Please use 'ask use <model>' first")
        return
    
    api_key = config.get_api_key(current_model)
    model_class = get_model_class(current_model)
    model = model_class(api_key)
    
    click.echo(f"Chatting with {current_model}. Type '/bye' to quit.")
    
    spinner = Halo(spinner='dots', text='Thinking...')
    
    while True:
        try:
            message = input(">>> ")
            if message.lower() == '/bye':
                break
            
            spinner.start()
            
            try:
                response = await model.chat(message)
            finally:
                spinner.stop()
            
            click.echo(response)
            
        except KeyboardInterrupt:
            spinner.stop()
            break
        except Exception as e:
            spinner.stop()
            click.echo(f"Error: {str(e)}")

def main():
    cli(obj={})

if __name__ == '__main__':
    main() 