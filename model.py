# from moviepy.editor import VideoFileClip

# def get_video_resolution(video_path):
#     try:
#         # Загружаем видеофайл
#         video_clip = VideoFileClip(video_path)

#         # Получаем разрешение видео
#         width = video_clip.size[0]
#         height = video_clip.size[1]

#         # Закрываем видеофайл
#         video_clip.close()

#         return width, height

#     except Exception as e:
#         print(f"Ошибка: {e}")
#         return None

# # Укажите путь к вашему видеофайлу
# # video_path = 'G:/auto-subs-desctop/videos/test.mp4'
# video_path = 'G:/auto-subs-desctop/videos/folder/v/juliaann5.mp4'
# resolution = get_video_resolution(video_path)

# if resolution:
#     print(f"Разрешение видео: {resolution[0]}x{resolution[1]}")

from abc import ABC
from typing import Dict, List, NoReturn, Tuple, Union


class FuzzyModelABC(ABC):
    pass

class SolveInputValueABC(ABC):
    pass

class DefuzzificationABC(ABC):
    pass

class MakeRuleBaseABC(ABC):
    pass


class Descriptor():

    def __set_name__(self, owner: FuzzyModelABC, name: str) -> NoReturn:
        self.name = '_' + name
    
    def __get__(self, instance: FuzzyModelABC, owner: FuzzyModelABC) -> Union[List, int]:
        # print('__get__')
        return getattr(instance, self.name)

    def __set__(self, instance: FuzzyModelABC, value: Union[int, list, dict]) -> NoReturn:
        setattr(instance, self.name, value)
    


class FuzzyModel(FuzzyModelABC):

    x1 = Descriptor()
    x2 = Descriptor()
    border_for_first_term = Descriptor()
    border_for_second_term = Descriptor()
    border_for_output_term = Descriptor()

    __slots__ = ['_x1', '_x2', '_border_for_first_term', '_border_for_second_term', '_border_for_output_term']

    def __init__(
            self, 
            x1: int, 
            x2: int, 
            border_for_first_term: List[int], 
            border_for_second_term: List[int], 
            border_for_output_term: List[float],
            ):
        
        self.x1 = x1
        self.x2 = x2
        self.border_for_first_term = border_for_first_term
        self.border_for_second_term = border_for_second_term
        self.border_for_output_term = border_for_output_term
    
    def __getattribute__(self, item):
        return object.__getattribute__(self, item)
        

class SolveInputValueForModelWithTwoParameters(SolveInputValueABC):

    @classmethod
    def solve_input_value(cls, model: FuzzyModelABC):
        list_of_degrees_of_owned_for_first_parameter = cls.calculate_list_of_degrees_of_owned(model.x1, model.border_for_first_term)
        list_of_degrees_of_owned_for_second_parameter = cls.calculate_list_of_degrees_of_owned(model.x2, model.border_for_second_term)

        return list_of_degrees_of_owned_for_first_parameter, list_of_degrees_of_owned_for_second_parameter

    @staticmethod
    def calculate_degree_of_owned(x: int, border1: int, border2: int):
        return round((border2 - abs(x - border1)) / border2, 2)
    
    @classmethod
    def calculate_list_of_degrees_of_owned(cls, x: int, border: List[int]):
        list_of_degrees_of_owned = [0, 0, 0]

        if border[0] <= x <= border[1]:
            list_of_degrees_of_owned[0] = (cls.calculate_degree_of_owned(x, border[0], border[1]))
        if border[0] <= x <= border[2]:
            list_of_degrees_of_owned[1] = cls.calculate_degree_of_owned(x, border[1], border[1])
        if border[1] <= x <= border[2]:
            list_of_degrees_of_owned[2] = cls.calculate_degree_of_owned(x, border[2], border[1])

        return list_of_degrees_of_owned

        
class MakeRuleBase(MakeRuleBaseABC):

    @staticmethod
    def make_rule_base(A1: int, A2: int, A3: int,
             B1: int, B2: int, B3: int):
        
        result = [{"C2": A1 * B1},
            {"C1": A1 * B2},
            {"C1": A1 * B3},
            {"C3": A2 * B1},
            {"C2": A2 * B2},
            {"C1": A2 * B3},
            {"C3": A3 * B1},
            {"C2": A3 * B2},
            {"C2": A3 * B3}]
        
        new_values = list(map(lambda x: round(list(x.values())[0], 2), result))
        
        for i, dictionary in enumerate(result):
            for key in dictionary:
                dictionary[key] = new_values[i]
        
        return result
    
class DefuzzificationByHeightMethod(DefuzzificationABC):

    @staticmethod
    def execute_defuzzification(rule_base: List[Dict[str, float],], border_for_output_term: List[float]) -> float:
        result = []
        values_of_C1 = []
        values_of_C2 = []
        values_of_C3 = []
        
        for i in rule_base:
            if i.get("C1") != 0.0 and i.get("C2") != 0.0 and i.get("C3") != 0.0:
                result.append(i)
        for i in result:
            if i.get("C1", False):
                values_of_C1.append(i.get("C1"))
            elif i.get("C2", False):
                values_of_C2.append(i.get("C2"))
            elif i.get("C3", False):
                values_of_C3.append(i.get("C3"))      

        denominator = sum(values_of_C1) + sum(values_of_C2) + sum(values_of_C3)
        
        values_of_C1, values_of_C2, values_of_C3 = list(map(lambda x: x*border_for_output_term[0], values_of_C1)), list(map(lambda x: x*border_for_output_term[1], values_of_C2)), list(map(lambda x: x*border_for_output_term[2], values_of_C3))
        
        numerator = sum(values_of_C1) + sum(values_of_C2) + sum(values_of_C3)
        
        return round(numerator/denominator, 2)
    
    @staticmethod
    def calculate_degree_of_owned(x: int, border1: int, border2: int) -> float:
        return round((border2 - abs(x - border1)) / border2, 2)
    
    @classmethod
    def calculate_list_of_degrees_of_owned_for_output_parameter(cls, y: float, border_for_output_term: List[float]) -> List[float]:
        list_of_degrees_of_owned_for_output_parameter = [0, 0, 0]

        if border_for_output_term[0] <= y <= border_for_output_term[1]:
            list_of_degrees_of_owned_for_output_parameter[0] = (cls.calculate_degree_of_owned(y, border_for_output_term[0], border_for_output_term[1]))
        if border_for_output_term[0] <= y <= border_for_output_term[2]:
            list_of_degrees_of_owned_for_output_parameter[1] = cls.calculate_degree_of_owned(y, border_for_output_term[1], border_for_output_term[1])
        if border_for_output_term[1] <= y <= border_for_output_term[2]:
            list_of_degrees_of_owned_for_output_parameter[2] = cls.calculate_degree_of_owned(y, border_for_output_term[2], border_for_output_term[1])

        print("Степень принадлежности к терму 'Низкая загрузка': ", list_of_degrees_of_owned_for_output_parameter[0])
        print("Степень принадлежности к терму 'Средняя загрузка': ", list_of_degrees_of_owned_for_output_parameter[1])
        print("Степень принадлежности к терму 'Высокая загрузка': ", list_of_degrees_of_owned_for_output_parameter[2])

        return list_of_degrees_of_owned_for_output_parameter

    @classmethod
    def find_result_of_max_term(cls, y: float, border_for_output_term: List[float]) -> Tuple[Union[str, float]]:
        list_of_degrees_of_owned_for_output_parameter = cls.calculate_list_of_degrees_of_owned_for_output_parameter(y, border_for_output_term)
        result = {
                'C1': list_of_degrees_of_owned_for_output_parameter[0], 
                  'C2': list_of_degrees_of_owned_for_output_parameter[1], 
                  'C3': list_of_degrees_of_owned_for_output_parameter[2],
                  }

        values = list(result.values())
        keys = list(result.keys())
        maxi = max(result.values())

        for i in range(len(values)):
            if values[i] == maxi:
                index = i
                break

        key = keys[index]

        return key, y

    @classmethod
    def get_resulting_value(cls, rule_base: List[Dict[str, float],], border_for_output_term: List[float]) -> Tuple[Union[str, float]]:
        y = cls.execute_defuzzification(rule_base, border_for_output_term)

        return cls.find_result_of_max_term(y, border_for_output_term)




m = FuzzyModel(
    x1=20, 
    x2=76800, 
    border_for_first_term=[0, 15, 30], 
    border_for_second_term=[0, 777600, 2457600],
    border_for_output_term = [0, 0.5, 1] 
    )

result = SolveInputValueForModelWithTwoParameters.solve_input_value(m)
print(result)

print(MakeRuleBase.make_rule_base(result[0][0], result[0][1], result[0][2], result[1][0], result[1][1], result[1][2],))

result = MakeRuleBase.make_rule_base(result[0][0], result[0][1], result[0][2], result[1][0], result[1][1], result[1][2],)

print(DefuzzificationByHeightMethod.get_resulting_value(result, m.border_for_output_term))



