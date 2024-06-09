from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_USERS_DIR = BASE_DIR.joinpath('images/users')
IMAGES_PROJECTS_DIR = BASE_DIR.joinpath('images/projects')
DOCUMENTS_DIR = BASE_DIR.joinpath('documents/')
TEMP_DIR = BASE_DIR.joinpath('temp/')

# DEFAULT_PROFILE_PIC = BASE_DIR.joinpath('images/users/default/default.jpeg')
DEFAULT_PROFILE_PIC = "/images/default/profile_pic/profile_pic.jpeg"
DEFAULT_PROJECT_PIC = "/images/default/project_pic/project_pic.jpg"
DEFAULT_TASK_PIC = "/images/default/task_pic/task_pic.jpeg"

IMAGES_USERS_SIZE = (600, 300)
PROFILE_PIC_SIZE = (300, 300)
ALLOWED_CONTENT_TYPE = ['image/jpg', 'image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/bmp']