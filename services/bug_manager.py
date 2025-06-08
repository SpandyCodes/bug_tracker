from models.bug import Bug
from models.user import User
from models import db

class BugManager:
    def get_all_bugs(self):
        return Bug.query.order_by(Bug.created_at.desc()).all()

    def get_bugs_for_user(self, user):
        if user.is_admin():
            return self.get_all_bugs()
        # Regular user: bugs created by or assigned to them
        return Bug.query.filter(
            (Bug.creator_id == user.id) | (Bug.assignee_id == user.id)
        ).order_by(Bug.created_at.desc()).all()

    def get_bug_by_id(self, bug_id):
        return Bug.query.get(bug_id)

    def create_bug(self, title, description, creator_id):
        new_bug = Bug(title=title, description=description, creator_id=creator_id)
        db.session.add(new_bug)
        db.session.commit()
        return new_bug

    def update_bug(self, bug_id, **kwargs):
        bug = self.get_bug_by_id(bug_id)
        if not bug:
            return None
        for key, value in kwargs.items():
            if hasattr(bug, key):
                setattr(bug, key, value)
        db.session.commit()
        return bug

    def delete_bug(self, bug_id):
        bug = self.get_bug_by_id(bug_id)
        if not bug:
            return False
        db.session.delete(bug)
        db.session.commit()
        return True

    def assign_bug(self, bug_id, user_id):
        bug = self.get_bug_by_id(bug_id)
        user = User.query.get(user_id)
        if not bug or not user:
            return None
        bug.assignee_id = user_id
        db.session.commit()
        return user

    def unassign_bug(self, bug_id):
        bug = self.get_bug_by_id(bug_id)
        if not bug:
            return False
        bug.assignee_id = None
        db.session.commit()
        return True

    def update_progress_and_comments(self, bug_id, progress, comments):
        bug = self.get_bug_by_id(bug_id)
        if not bug:
            return None
        bug.progress = max(0, min(100, int(progress)))  # Clamp between 0-100
        bug.comments = comments
        if bug.progress == 100:
            bug.status = 'Closed'
        elif bug.progress > 0:
            bug.status = 'In Progress'
        db.session.commit()
        return bug
