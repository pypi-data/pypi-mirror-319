from mgraph_ai.mgraph.domain.MGraph__Node                             import MGraph__Node
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Node          import Model__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Shape import Schema__Mermaid__Node__Shape

LINE_PADDING = '    '

class Mermaid__Node(MGraph__Node):
    model : Model__Mermaid__Node

    def config(self):
        return self.model.config

    def markdown(self, value=True):
        self.config().markdown = value
        return self

    def shape(self, shape=None):
        self.config().node_shape = Schema__Mermaid__Node__Shape.get_shape(shape)
        return self


    def shape_asymmetric        (self): self.config().node_shape = Schema__Mermaid__Node__Shape.asymmetric        ; return self
    def shape_circle            (self): self.config().node_shape = Schema__Mermaid__Node__Shape.circle            ; return self
    def shape_cylindrical       (self): self.config().node_shape = Schema__Mermaid__Node__Shape.cylindrical       ; return self
    def shape_default           (self): self.config().node_shape = Schema__Mermaid__Node__Shape.default           ; return self
    def shape_double_circle     (self): self.config().node_shape = Schema__Mermaid__Node__Shape.double_circle     ; return self
    def shape_hexagon           (self): self.config().node_shape = Schema__Mermaid__Node__Shape.hexagon           ; return self
    def shape_parallelogram     (self): self.config().node_shape = Schema__Mermaid__Node__Shape.parallelogram     ; return self
    def shape_parallelogram_alt (self): self.config().node_shape = Schema__Mermaid__Node__Shape.parallelogram_alt ; return self
    def shape_stadium           (self): self.config().node_shape = Schema__Mermaid__Node__Shape.stadium           ; return self
    def shape_subroutine        (self): self.config().node_shape = Schema__Mermaid__Node__Shape.subroutine        ; return self
    def shape_rectangle         (self): self.config().node_shape = Schema__Mermaid__Node__Shape.rectangle         ; return self
    def shape_rhombus           (self): self.config().node_shape = Schema__Mermaid__Node__Shape.rhombus           ; return self
    def shape_round_edges       (self): self.config().node_shape = Schema__Mermaid__Node__Shape.round_edges       ; return self
    def shape_trapezoid         (self): self.config().node_shape = Schema__Mermaid__Node__Shape.trapezoid         ; return self
    def shape_trapezoid_alt     (self): self.config().node_shape = Schema__Mermaid__Node__Shape.trapezoid_alt     ; return self



    def wrap_with_quotes(self, value=True):
        self.config().wrap_with_quotes = value
        return self

    def show_label(self, value=True):
        self.config().show_label = value
        return self