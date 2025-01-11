use crate::types::v0_4_0::{Factor, VFG};
use crate::types::{Metadata, ModelType};
use pyo3::types::PyDict;
use pyo3::{pymethods, Bound};
use crate::types::v0_2_0::python::convert_variables_from_pydict;

#[pymethods]
impl VFG {
    #[new]
    fn new(factors: Vec<Factor>, variables: Bound<PyDict>, metadata: Option<Metadata>, visualization_metadata: Option<String>) -> Self {
        let variables = convert_variables_from_pydict(variables);
        VFG { version: crate::loader::VFG_VERSION.to_string(), factors, variables, metadata, visualization_metadata }
    }

    #[staticmethod]
    #[pyo3(name = "default")]
    fn py_default() -> Self {
        Self::default()
    }
}

#[pymethods]
impl Metadata {
    #[new]
    fn new(model_type: Option<ModelType>, model_version: Option<String>, description: Option<String>) -> Self {
        Metadata { model_type, model_version, description }
    }

    #[staticmethod]
    #[pyo3(name = "default")]
    fn py_default() -> Self { Self::default() }
}
