import os
import time
from loguru import logger
import praw
from vegmod.serializer import serialize, serialize_list
from vegmod.utils import save_dict
from vegmod.cache import Cache

DATA_DIR = f"{os.path.dirname(__file__)}/../data"
INGRESS_FILE_PATH=f"{DATA_DIR}/ingress.json"
CACHE_FILE_PATH=f"{DATA_DIR}/ingress_cache.json"
REQUEST_DELAY = 1

def pull(subreddits: list[praw.models.Subreddit]):
    """
    Pull data from the subreddits and save it to a JSON file.
    """
    run_id = int(time.time())
    save_run_id(run_id)
    
    data = {}
    for subreddit in subreddits:        
        cache = Cache(CACHE_FILE_PATH)
        try:
            logger.info(f"Pulling subreddit={subreddit.display_name}")
            subreddit_data = serialize(subreddit, cache=cache)
            time.sleep(REQUEST_DELAY)

            logger.info(f"Pulling subreddit={subreddit.display_name} submissions")
            submissions = list(subreddit.new(limit=25))
            subreddit_data["submissions"] = serialize_list(submissions, cache=cache)
            time.sleep(REQUEST_DELAY)

            logger.info(f"Pulling subreddit={subreddit.display_name} comments")
            comments = list(subreddit.comments(limit=100)) # 100 gives longer score updates
            subreddit_data["comments"] = serialize_list(comments, cache=cache)
            time.sleep(REQUEST_DELAY)

            logger.info(f"Pulling subreddit={subreddit.display_name} removal reasons")
            removal_reasons = list(subreddit.mod.removal_reasons)
            subreddit_data["removal_reasons"] = serialize_list(removal_reasons, cache=cache)
            time.sleep(REQUEST_DELAY)

            logger.info(f"Pulling subreddit={subreddit.display_name} rules")
            rules = list(subreddit.rules)
            subreddit_data["rules"] = serialize_list(rules, cache=cache)
            time.sleep(REQUEST_DELAY)
            
            logger.info(f"Pulling subreddit={subreddit.display_name} widgets.sidebar")
            widgets_sidebar = list(subreddit.widgets.sidebar)
            subreddit_data["widgets_sidebar"] = serialize_list(widgets_sidebar, cache=cache)
            time.sleep(REQUEST_DELAY)
            
            logger.info(f"Pulling subreddit={subreddit.display_name} moderators")
            subreddit_data["moderators"] = serialize_list(list(subreddit.moderator()), cache=cache)

            data[subreddit.display_name] = subreddit_data
        except Exception as e:
            logger.error(f"Error pulling subreddit={subreddit.display_name} error={e}")
            
            # if data has a key for the subreddit, remove it
            if subreddit.display_name in data:
                del data[subreddit.display_name]
            
            continue            
        finally:
            # if the run_id has changed, stop to preserve API quota
            # also don't save cache if the run_id has changed, as it will cause cache inconsistency
            if load_run_id() != run_id:
                logger.info(f"Run ID changed, new process started, stopping to preserve API quota")
                return
            else:
                logger.info(f"Saving cache")
                cache.save()
                logger.info(f"Cache saved")

    save_dict(data, INGRESS_FILE_PATH)
    
def save_run_id(run_id: int):
    # save a text file with the run_id
    with open(f"{DATA_DIR}/run_id.txt", "w") as f:
        f.write(str(run_id))

def load_run_id():
    # load the run_id from the text file
    with open(f"{DATA_DIR}/run_id.txt", "r") as f:
        return int(f.read())
