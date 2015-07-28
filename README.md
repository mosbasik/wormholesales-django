# django-app-template
Basic structure of a django app, for reuse when starting new apps.

## How to Use:

1. (Optional): Make a github repository if you want to keep this project online.

1. Make a virtual python environment on your machine using the repository name you intend to use for this project: `mkproject repository_name`.  To do this you need to have `virtualenv` and `virtualenvwrapper` installed for your system's Python environment.  To know if you have these already, check if they show up when you run `pip freeze`.  You need `pip` installed, of course.  If you don't have them, run `pip install virtualenv virtualenvwrapper`.

1. Go up one level, out of your project folder that was just created (`cd ..`) and delete it: `rmdir repository_name`.

1. Clone this repository, using your project's name: `git clone git@github.com:mosbasik/django-app-template.git repository_name`.

1. Enter your local repo (`cd repository_name`).  If you made a GitHub repo in step one, set your local repo's origin remotes to it, preferably using the SSH link: `git remote set-url origin git@github.com:USERNAME/OTHERREPOSITORY.git`.

1. Install Django and the Python MySQL bindings by running `pip install -r reqs.txt` while in the top folder of your repo.  You will get the versions specified in `reqs.txt`.
