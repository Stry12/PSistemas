import unittest
import grpc
import distance_unary_pb2_grpc as pb2_grpc
import distance_unary_pb2 as pb2
from google.protobuf.json_format import MessageToJson
import json

BASE_URL = "localhost:50051/"

class TestDistanceService(unittest.TestCase):

    def setUp(self): #Cambiar a setupbeforeclass
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = pb2_grpc.DistanceServiceStub(self.channel)

    ##UNIDAD DE MEDIDA VACIA

    def test_distance_not_unit(self):
        request = pb2.SourceDest(
            source=pb2.Position(
                latitude=90, longitude=-70.5955963
            ),
            destination=pb2.Position(
                latitude=-33.0348327, longitude=-71.5980458
            ),
            unit=None
        )

        print("prueba: distancia sin unidad")
        response = self.stub.geodesic_distance(request)
        print(response)
        self.assertEqual(response.unit,"km")

    ##Unidad de medida invalida

    def test_distance_unit_invalid(self):
        request = pb2.SourceDest(
            source=pb2.Position(
                latitude=20, longitude=180
            ),
            destination=pb2.Position(
                latitude=-33.0348327, longitude=-71.5980458
            ),
            unit="mi"
        )

        print("prueba unidad no válida")
        response = self.stub.geodesic_distance(request)
        print(response)
        self.assertEqual(response.distance, -1.0)

    ##Calculo correcto en nm
    ##Son millas nauticas modificar, y dar rango de flexibilidad
    def test_distance_corrcalnm(self):
        request = pb2.SourceDest(
            source=pb2.Position(
                latitude=-33.075607, longitude=-71.469818
            ),
            destination=pb2.Position(
                latitude=-33.075535, longitude=-71.458746
            ),
            unit="nm"
        )

        print("cálculo en millas náuticas")
        response = self.stub.geodesic_distance(request)
        print(response)
        self.assertEqual((0.5 < response.distance < 0.6), True)


    ##Fuera del limite

    def test_distance_border_latitud_One(self):
        request = pb2.SourceDest(
            source=pb2.Position(
                latitude=91, longitude=-70.5955963
            ),
            destination=pb2.Position(
                latitude=-33.0348327, longitude=-71.5980458
            ),
            unit="km"
        )

        print("prueba de latitud")
        response = self.stub.geodesic_distance(request)
        print(response)
        self.assertEqual(response.distance, -1.0)


    def test_distance_border_Latitud_Two(self):
        request = pb2.SourceDest(
            source=pb2.Position(
                latitude=-91, longitude=20
            ),
            destination=pb2.Position(
                latitude=-33.0348327, longitude=-71.5980458
            ),
            unit="km"
        )

        print("segunda prueba de latitud")
        response = self.stub.geodesic_distance(request)
        print(response)
        self.assertEqual(response.distance, -1.0)

    def test_distance_border_Logitude_One(self):
        request = pb2.SourceDest(
            source=pb2.Position(
                latitude=20, longitude=-181
            ),
            destination=pb2.Position(
                latitude=-33.0348327, longitude=-71.5980458
            ),
            unit="km"
        )

        print("primera prueba de longitud")
        response = self.stub.geodesic_distance(request)
        self.assertEqual(response.distance, -1.0)


    def test_distance_border_Logitude_two(self):
        request = pb2.SourceDest(
            source=pb2.Position(
                latitude=20, longitude=181
            ),
            destination=pb2.Position(
                latitude=-33.0348327, longitude=-71.5980458
            ),
            unit="km"
        )

        print("segunda prueba de longitud")
        response = self.stub.geodesic_distance(request)
        print(response)
        self.assertEqual(response.distance, -1.0)

    ##Limites

    def test_distance_border_Logitude_limit(self):
        request = pb2.SourceDest(
            source=pb2.Position(
                latitude=20, longitude=180
            ),
            destination=pb2.Position(
                latitude=-33.0348327, longitude=-71.5980458
            ),
            unit="km"
        )

        print("prueba limite de longitud")
        response = self.stub.geodesic_distance(request)
        print(response)
        self.assertAlmostEqual(response.distance, 12876.58, delta = 0.5)

    def test_distance_border_Latitud_limit(self):
        request = pb2.SourceDest(
            source=pb2.Position(
                latitude=-90, longitude=20
            ),
            destination=pb2.Position(
                latitude=-33.0348327, longitude=-71.5980458
            ),
            unit="km"
        )
        print("prueba limite de latitud")
        response = self.stub.geodesic_distance(request)
        print(response)
        self.assertAlmostEqual(response.distance, 6345.37, delta = 0.5)


    def tearDown(self):
        # Cierra el canal gRPC
        self.channel.close()

if __name__ == '__main__':
    unittest.main()
