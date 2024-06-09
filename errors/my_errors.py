from fastapi import HTTPException, status

USERNAME_IS_OCCUPIED_ERROR = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is occupied by another person.")
INCORRECT_UN_OR_PSWD_ERROR = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password.",headers={"WWW-Authenticate": "Bearer"},)

USER_NOT_EXIST_ERROR = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist.")

TASK_NOT_EXIST_ERROR = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task doesn't exist.")
SUBTASK_NOT_EXIST_ERROR = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subtask doesn't exist.")

PROJECT_NOT_EXIST_ERROR = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project doesn't exist.")
PERMISSION_DENIED_ERROR = HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Permission denied.")

USER_IS_ALREADY_A_MEMBER = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already a member of the project.")
USER_IS_NOT_A_MEMBER = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is not a project member.")
SUICIDE_IS_NOT_A_WAY_OUT = HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can't delete yourself from your own project.")

FILE_IS_NOT_AN_IMAGE = HTTPException(status_code=400, detail="The file you tried to upload is not an image.")
IMAGE_TYPE_NOT_ALLOWED = HTTPException(status_code=400, detail="Image type not allowed.")

FILE_IS_INFECTED = HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The file is infected.")
FILE_IS_NOT_EXIST = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File doesn't exist.")
USER_IS_ALREADY_HAS_FILE = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already has access to the file.")