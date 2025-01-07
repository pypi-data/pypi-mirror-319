use ::scala_native_demangle as rs_library;
use pyo3::exceptions::*;
use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn demangle_with_defaults(a: String) -> PyResult<String> {
    match rs_library::demangle_with_defaults(a.as_str()) {
        Ok(res) => Ok(res),
        Err(e) => Err(PyValueError::new_err(e)),
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn scala_native_demangle(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(demangle_with_defaults, m)?)?;
    Ok(())
}
