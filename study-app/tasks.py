from invoke import task

@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)

@task
def build(ctx):
    ctx.run("python3 src/build.py", pty=True)