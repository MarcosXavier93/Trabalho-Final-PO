from __future__ import division
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import requests
import json
import urllib
import numpy as np 
import matplotlib.pyplot as plt 
from docplex.mp.model import Model
import sys
import cplex
from cplex.exceptions import CplexError

def modelo_dados():
    
    data = {}
    data['matriz_distancias'] = [
                    [0, 145965, 174309, 193014, 67981, 404421, 51265, 108223, 217859, 103292, 97172, 116474, 176081, 131390, 239297, 230703, 159832, 225014],
                    [153328, 0, 28939, 301572, 139593, 470818, 102639, 216781, 220213, 77975, 51312, 115788, 178435, 133744, 347856, 282609, 211739, 276921],
                    [180079, 29100, 0, 328323, 166344, 495596, 129391, 243532, 246964, 104726, 78063, 142540, 221209, 160496, 374607, 309360, 238490, 303672],
                    [192713, 300477, 328821, 0, 146875, 263074, 242776, 85587, 191492, 223375, 288684, 183614, 171884, 163132, 75526, 388410, 319906, 382722],
                    [67784, 138495, 166840, 146329, 0, 357736, 117847, 63330, 157280, 61393, 141363, 54686, 115502, 69602, 192613, 263481, 194977, 257793],
                    [403571, 490547, 513882, 262557, 357734, 0, 453634, 296445, 259641, 434233, 499542, 366668, 306465, 346186, 197114, 599269, 530764, 593580],
                    [51599, 96095, 124439, 243410, 118378, 454818, 0, 158619, 215668, 74681, 47303, 111243, 173890, 129199, 289694, 190609, 119738, 184920],
                    [108259, 216022, 244367, 85547, 64513, 296954, 158322, 0, 131300, 138920, 204229, 101251, 89522, 80769, 131831, 303956, 235451, 298268],
                    [237527, 219376, 247720, 191400, 157712, 260230, 215681, 131574, 0, 142274, 222243, 107493, 47291, 87012, 125957, 419282, 348412, 413593],
                    [122899, 77102, 105447, 223597, 61618, 435004, 75071, 138806, 142238, 0, 79970, 37813, 100460, 55770, 269881, 278671, 207801, 272983],
                    [103918, 50565, 78909, 295730, 141422, 507137, 53230, 210939, 222042, 79804, 0, 117617, 180264, 135573, 342014, 233199, 162329, 227511],
                    [125110, 114421, 142765, 183691, 63829, 367082, 110726, 100692, 107319, 37318, 117288, 0, 65541, 20850, 229975, 314327, 243456, 308638],
                    [195235, 177084, 205428, 172281, 115420, 307036, 173390, 89282, 47273, 99982, 179952, 65202, 0, 44720, 172764, 376990, 306120, 371302],
                    [141397, 133700, 162044, 163268, 75406, 346659, 130005, 80269, 86896, 56598, 136567, 21817, 45117, 0, 209551, 333606, 262735, 327917],
                    [239216, 346980, 375324, 75801, 193378, 197744, 289279, 132090, 126167, 269878, 335187, 233194, 172991, 212712, 0, 434913, 366409, 429225],
                    [232159, 283647, 311991, 373455, 248423, 584862, 192076, 288664, 421787, 280800, 234855, 317362, 380009, 335318, 419739, 0, 76027, 22460],
                    [162268, 213757, 242101, 322323, 197290, 533730, 122186, 237532, 351897, 210910, 164965, 247472, 310119, 265428, 368607, 74970, 0, 69282],
                    [223688, 275177, 303521, 380923, 255890, 592330, 183606, 296132, 413317, 272330, 226384, 308892, 371539, 326848, 427207, 19008, 67556, 0]
                ]
    data['numero_veiculos'] = 1
    data['depot'] = 0
    return data


def mostrar_solucao(manager, routing, assignment):

    print('Resultado da Funcao Objetivo: {} Kilometros'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Melhor Rota Encontrada :'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Resultado da Funcao Objetivo: {}Kilometros\n'.format(route_distance)
'''
                                 #['824F+56+Maripa+de+Minas+MG',  # Oxetil, pontoDePartida
                                # MG
                                'Barbacena+MG',  # BARBACENA
                                'Barroso+MG',  # BARROSO
                                'Carangola+MG',  # CARANGOLA
                                'Cataguases+MG',  # CATAGUASES
                                'Governador+Valadares+MG',  # GOVERNADOR VALADARES
                                'Juiz+de+Fora+MG',  # Juiz de Fora
                                'Muriae+MG',  # MURIAE
                                'Ponte+Nova+MG',  # PONTE NOVA
                                'Rio+Pomba+MG',  # RIO POMBA
                                'Santos+Dumont+MG',  # SANTOS DUMONT
                                'Uba+MG',  # UBA
                                'Vicosa+MG',  # VICOSA
                                'Visconde+do+Rio+Branco+MG',  # VISCONDE DO RIO BRANCO
                                # RJ
                                'Manhuacu+RJ',  # MANHUACU
                                'Niteroi+RJ',  # NITEROI
                                'Petropolis+RJ',  # PETROPOLIS
                                'Rio+de+Janeiro+RJ'  # RIO DE JANEIRO
                                ]#
                                '''
def main():
    print("Mostrando a Melhor Solucao CPLEX")
    data = modelo_dados()

    manager = pywrapcp.RoutingIndexManager(len(data['matriz_distancias']),
                                           data['numero_veiculos'], data['depot'])


    routing = pywrapcp.RoutingModel(manager)


    def mostra_dstancia(from_index, to_index):
      
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['matriz_distancias'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(mostra_dstancia)


    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

  
    assignment = routing.SolveWithParameters(search_parameters)

  
    if assignment:
        mostrar_solucao(manager, routing, assignment)

if __name__ == '__main__':
    main()
