from awesomeNations.nationMethods import N
from awesomeNations.regionMethods import R
from typing import Iterator
from datetime import datetime

class AwesomeNations:
    """
    Hello! I'm the main class of this library and I'm very excited to work with you!
    """
    def nationStates_birthday() -> bool:
        "Today is 11/13?"
        today = datetime.today()
        date: str = today.strftime('%D')
        birthday: bool = False
        if '11/13' in date:
            birthday = True
        return birthday

    def nationStates_age() -> str:
        "Current year - NationStates year of creation (NationStates was created in 2002)."
        created = 2002
        today = datetime.today().year
        age = today - created
        result = f'Around {age-1}-{age} years old.'
        return result

    class Nation:
        """
        Class dedicated to extracting data from NationStates nations.
        """
        def __init__(self, nation_name: str = 'testlandia') -> None:
            self.nation_name = nation_name

        def exists(self) -> bool:
            """
            Checks if nation exists.
            """
            exist = N(self.nation_name).exists()
            return exist
        
        def get_overview(self) -> dict:
            """
            Get an overview of the requested nation.
            """
            overview = N(self.nation_name).overview()
            return overview

        def get_activity(self, filters: str = 'all') -> Iterator:
            """
            Get national happenings of the requested nation.
            """
            activity = N.activity(self, filters)
            return activity

        def get_census(self, censusid: tuple | list = [0]) -> Iterator:
            """
            Gets one or more censuses [0-88] from the requested nation, examples:
            - [0]: Civil rights
            - [46]: Defense Forces
            - [0, 1, 2, 3] ... [88]
            """
            census = N(self.nation_name).census_generator(censusid)
            return census

    class Region:
        """
        Class dedicated to extracting data from NationStates regions.
        """
        def __init__(self, region_name: str = 'The Pacific') -> None:
            self.region_name = region_name
        
        def exists(self) -> bool:
            """
            Checks if the region exists.
            """
            exist = R.exists(self)
            return exist
        
        def get_overview(self) -> dict:
            """
            Provides an overview of the requested region.
            """
            overview = R.overview(self)
            return overview

        def get_world_census(self, censusid: tuple | list = [0]) -> Iterator:
            """
            Retrieves a world census of the requested region.
            """
            ranks = R.world_census(self, censusid)
            return ranks

        def get_activity(self, filters: str = 'all') -> Iterator:
            """
            Get regional happenings of the requested region.
            """
            activity = R.activity(self, filters)
            return activity

        def get_embassies(self) -> Iterator:
            """
            Retrieves embassies of the requested region.
            """
            embassies = R.embassies(self)
            return embassies

# Testing to see if my life is worth it:
if __name__ == '__main__':
    nation = (AwesomeNations.Nation('testlandia'))
    region = (AwesomeNations.Region('The Pacific'))

    print('NATION:')
    print(f'{nation.exists()=}\n')
    print(f'{nation.get_overview()=}\n')
    for activity in nation.get_activity():
        print(activity)
    print('\n')
    for census in nation.get_census([i for i in range(21)]):
        print(census)
    
    print('REGION:')
    print(f'{region.exists()=}\n')
    print(f'{region.get_overview()=}\n')
    for activity in region.get_activity():
        print(activity)
    for embassy in region.get_embassies():
        print(embassy)
    for rank in AwesomeNations.Region().get_world_census([i for i in range(21)]):
        print(rank, '\n')