from abc import abstractmethod
from typing import Optional, List
from app.repositories.base import InMemoryRepository, IRepository
from app.domain.course.model import Course
from app.data.course_seed import SEED_COURSE

class ICourseRepository(IRepository[Course]):

    @abstractmethod
    def find_by_name(self,name:str) -> Optional[Course]:
        pass

    @abstractmethod
    def next_id(self) -> int:
        pass

    @abstractmethod
    def search(self, q: str) -> List[Course]:
        pass

class CourseRepositoty(InMemoryRepository[Course], ICourseRepository):

    def __init__(self, seed):
        super().__init__()

        for row in seed or []:
            course = Course(**row)
            self._items[course.id]= course

    def next_id(self) ->int:
        if not self._items:
            return 1
        return max(self._items.keys()) + 1

    def find_by_name(self, name: str) -> Optional[Course]:
        clean_name = name.strip().lower()
        return next(
            ( 
                course 
                for course in self._items.values()
                if  course.name.lower() == clean_name
            ),None,
            
        )

    def search(self, q: str) -> List[Course]:
        clean_q = q.strip().lower()
        return [
            course 
            for course in self._items.values()
            if clean_q in course.name.lower() 
        ]
course_repo: ICourseRepository = CourseRepositoty(seed=SEED_COURSE)