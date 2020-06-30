from tensorflow.keras import backend as K
from tensorflow.keras.layers import Input, Lambda, Add

from atomic_images.layers import DistanceMatrix, Unstandardization
from tfn.layers import MolecularSelfInteraction

from . import Builder


class TSBuilder(Builder):
    def __init__(self, *args, **kwargs):
        self.output_type = kwargs.pop('output_type', 'dist_matrix')  # [dist_matrix, energy, both]
        super().__init__(*args, **kwargs)

    def get_inputs(self):
        return [
            Input([self.num_atoms, ], name='atomic_nums', dtype='int32'),
            Input([self.num_atoms, 3], name='reactant_cartesians', dtype='float32'),
            Input([self.num_atoms, 3], name='product_cartesians', dtype='float32')
        ]

    def get_dual_trunks(self, point_clouds: list):
        embedding_layer = MolecularSelfInteraction(self.embedding_units, name='embedding')
        embeddings = [embedding_layer(
            pc, Lambda(lambda x: K.expand_dims(x, axis=-1))(pc))
            for pc in point_clouds]
        layers = self.get_layers()
        inputs = [self.get_learned_tensors(e, pc, layers)
                  for e, pc in zip(embeddings, point_clouds)]
        return inputs

    def get_learned_output(self, inputs: list):
        z, r, p = inputs
        point_clouds = [self.point_cloud_layer([x, z]) for x in (r, p)]
        inputs = self.get_dual_trunks(point_clouds)
        return point_clouds, inputs

    def get_model_output(self, point_cloud: list, inputs: list):
        one_hot = point_cloud[0][0]
        tensors = Add()(inputs)
        tensors = self.get_final_output(one_hot, tensors)
        outputs = []
        if self.output_type == 'dist_matrix' or self.output_type == 'both':
            cartesians = Lambda(lambda x: K.squeeze(x, axis=-2), name='cartesians')(tensors[-1])
            dist_matrix = DistanceMatrix(name='distance_matrix')(cartesians)
            outputs.append(dist_matrix)
        if self.output_type == 'energy' or self.output_type == 'both':
            atomic_energy = Lambda(lambda x: K.squeeze(x, axis=-1), name='atomic_energy')(
                tensors[0])
            atomic_energy = Unstandardization(self.mu, self.sigma, trainable=self.trainable_offsets)(
                [one_hot, atomic_energy]
            )
            molecular_energy = Lambda(lambda x: K.sum(x, axis=-2), name='molecular_energy')(
                atomic_energy)
            outputs.append(molecular_energy)
        if self.output_type not in ('dist_matrix', 'energy', 'both'):
            raise ValueError(
                'kwarg `output_type` has unknown value: {}'.format(str(self.output_type)))

        return outputs


class TSSiameseClassifierBuilder(TSBuilder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.final_si_units = 1

    def get_inputs(self):
        return [
            Input([2, self.num_atoms, ], name='atomic_nums', dtype='int32'),
            Input([2, self.num_atoms, 3], name='cartesians', dtype='float32')
        ]

    def get_learned_output(self, inputs: list):
        z, c = inputs
        point_clouds = [self.point_cloud_layer([a, b])
                        for a, b in zip(
                [c[:, 0], c[:, 1]], z[:, 0], z[:, 1]  # Split z, c into 4 arrays
            )]
        inputs = self.get_dual_trunks(point_clouds)
        return point_clouds, inputs

    def get_model_output(self, point_cloud: list, inputs: list):
        one_hot = point_cloud[0][0]
        tensors = Lambda(lambda x: K.abs(x[1] - x[0]))(inputs)  # absolute difference
        pass  # TODO: Pick up here!


# Different from existing TSBuilders
class TSClassifierBuilder(Builder):
    def get_inputs(self):
        return [
            Input([self.num_atoms, ], name='atomic_nums', dtype='int32'),
            Input([self.num_atoms, 3], name='cartesians', dtype='float32')
        ]

    def get_model_output(self, point_cloud: list, inputs: list):
        pass  # TODO: Implement this!
