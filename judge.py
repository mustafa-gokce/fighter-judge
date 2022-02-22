from dataclasses import dataclass
import time

# team structure to keep track data of team individually
@dataclass
class Team:
    id: int
    user_name: str
    login_time: dict
    prev_telem_data: dict = None
    curr_telem_data: dict = None
    prev_lock_on_data: dict = None
    curr_lock_on_data: dict = None
    last_delay: int = None
    logout_time: str = None
    score: int = 0


class Judge:
    registered_teams = list()

    # register the user to registered_team
    @classmethod
    def register_user(cls, user, login_time):
        team = Team(id=user.id, user_name=user.username, login_time=login_time)
        cls.registered_teams.append(team)

    @classmethod
    def remove_user(cls, user):

        for team in cls.registered_teams:

            if team.user_name == user.username:

                cls.registered_teams.remove(team)

    # save telemetry data of the team
    @classmethod
    def register_telem_data(cls, telem_data):

        for team in cls.registered_teams:

            # If specified team in registered teams
            if team.id == telem_data["takim_numarasi"]:

                # Update telemetry data but keep previous one
                team.prev_telem_data = team.curr_telem_data
                team.curr_telem_data = telem_data

        cls.__update_scores()

    # update score table by using current datas of teams
    @classmethod
    def __update_scores(cls):

        for team in cls.registered_teams:

            if team.prev_telem_data is not None:

                # calculate time difference in terms of ms
                delta_time = (team.curr_telem_data["GPSSaati"]["saat"] * 3600000 +
                              team.curr_telem_data["GPSSaati"]["dakika"] * 60000 +
                              team.curr_telem_data["GPSSaati"]["saniye"] * 1000 +
                              team.curr_telem_data["GPSSaati"]["milisaniye"]) \
                             - \
                             (team.prev_telem_data["GPSSaati"]["saat"] * 3600000 +
                              team.prev_telem_data["GPSSaati"]["dakika"] * 60000 +
                              team.prev_telem_data["GPSSaati"]["saniye"] * 1000 +
                              team.prev_telem_data["GPSSaati"]["milisaniye"])

                # to keep track delay of each team
                team.last_delay = delta_time

                # If update frequency is between 1Hz and 2Hz
                if 500 <= delta_time <= 1000:
                    team.score += 1
                else:
                    team.score -= 1

            if team.curr_lock_on_data is not None:
                team.score += 10

    # it returns score table
    @classmethod
    def get_scores(cls) -> dict:
        temp_dict = dict()
        for team in cls.registered_teams:
            temp_dict[f"{team.user_name}"] = team.score

        res = {"puanlar":temp_dict}

        return res

    # it returns delay table
    @classmethod
    def get_delays(cls) -> dict:
        temp_dict = dict()
        for team in cls.registered_teams:
            temp_dict[f"{team.user_name}"] = team.last_delay

        res = {"gecikmeler": temp_dict}

        return res
