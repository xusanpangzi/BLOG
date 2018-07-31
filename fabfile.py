from fabric.api import env,run
from fabric.operations import sudo

GIT_REPO = "https://github.com/xusanpangzi/Blog.git"

env.user = 'sanpangzi'
env.password = 'xuyameng32386964'

env.hosts = ['三胖子.xyz']

env.port = '27681'

def deploy():
    source_folder = '/home/sanpangzi/sites/三胖子.xyz/Blog'
    run("""
       cd {} &&
        ../env/bin/pip install -r requirements.txt &&
       ../env/bin/python3 manage.py collectstatic --noinput &&
       ../env/bin/python3 manage.py migrate
       ../env/bin/gunicorn --bind unix:/tmp/三胖子.xyz.socket Blog.wsgi:application --reload&
       """.format(source_folder))
    sudo('service nginx reload')