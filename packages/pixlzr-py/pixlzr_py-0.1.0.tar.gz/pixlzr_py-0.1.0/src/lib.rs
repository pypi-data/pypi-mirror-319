use image::{DynamicImage, RgbImage, RgbaImage};
use pixlzr::Pixlzr;
use pyo3::{exceptions::PyTypeError, prelude::*};

type PyImageBuffer = ((u32, u32), Vec<u8>);

/*
 * PIXLZR functions to expose:
 * - [x] encode_to_vec(&self) -> Raw
 * - [x] decode_from_vec(inp: Raw) -> Self
 *
 * - [x] open(path) -> Self
 * - [x] save(&self, path)
 *
 * - [ ] expand(&self, filter: FilterType) -> Self
 * - [ ] shrink(&mut self, filter_downscale: FilterType, before_average, after_average) -> ()
 * - [ ] shrink_by(&mut self, filter_downscale: FilterType, factor: f32) -> ()
 * - [ ] shrink_directionally(&mut self, filter_downscale: FilterType, factor: f32) -> ()
 *
 * - [ ] from_image(image: &DynamicImage, block_width: u32, block_height: u32) -> Self
 * - [ ] to_image(&self, filter: FilterType) -> DynamicImage
 *
*/

/// Encodes a imagebuffer into a Pixlzr image, and saves it to a file.
#[pyfunction]
#[pyo3(
    signature = (size, data, block_size = (32, 32), /, shrink = false, shrinking_factor = 1., filter_type = 3),
    text_signature = "(size, data, block_size = (32, 32), /, shrink = false, shrinking_factor = 1., filter_type = 3)"
)]
fn encode_image(
    size: (u32, u32),
    data: &[u8],
    block_size: (u32, u32),
    shrink: bool,
    shrinking_factor: f32,
    filter_type: u8,
) -> PyResult<Vec<u8>> {
    let is_rgba = data.len() as u32 == size.0 * size.1 * 4;
    // Creates Pixlzr image
    let img = if is_rgba {
        let rgba = RgbaImage::from_raw(size.0, size.1, data.to_vec()).unwrap();
        DynamicImage::ImageRgba8(rgba)
    } else {
        let rgb = RgbImage::from_raw(size.0, size.1, data.to_vec()).unwrap();
        DynamicImage::ImageRgb8(rgb)
    };
    let mut img = Pixlzr::from_image(&img, block_size.0, block_size.1);
    // Saves encoded Pixlzr to file
    if shrink {
        img.shrink_by(filter_type.into(), shrinking_factor);
    }

    img.encode_to_vec()
        .map_err(|e| PyTypeError::new_err(e.to_string()))
}

/// Decodes a Pixlzr image from a buffer.
#[pyfunction]
#[pyo3(signature = (buffer, filter_type = 3), text_signature = "(buffer, filter_type = 3)")]
fn decode_buffer_into_image(buffer: &[u8], filter_type: u8) -> PyResult<PyImageBuffer> {
    let img = Pixlzr::decode_from_vec(buffer.to_vec())
        .map_err(|_| PyTypeError::new_err("Error decoding."))?;
    let bytes = img
        .expand(filter_type.into())
        .blocks
        .iter()
        .flat_map(|block| block.as_slice().to_owned())
        .collect::<Vec<u8>>();
    Ok((img.dimensions(), bytes))
}

/// Reads a Pixlzr image from a file, and returns an imagebuffer.
#[pyfunction]
#[pyo3(signature = (path, filter_type = 3), text_signature = "(path, filter_type = 3)")]
fn open_image(path: &str, filter_type: u8) -> PyResult<PyImageBuffer> {
    let img = Pixlzr::open(path).map_err(|_| PyTypeError::new_err("Error reading."))?;
    let bytes = img
        .expand(filter_type.into())
        .blocks
        .iter()
        .flat_map(|block| block.as_slice().to_owned())
        .collect::<Vec<u8>>();
    Ok((img.dimensions(), bytes))
}

/// Encodes a imagebuffer into a Pixlzr image, and saves it to a file.
#[pyfunction]
#[pyo3(
    signature = (path, size, data, block_size = (32, 32), /, shrink = false, shrinking_factor = 1., filter_type = 3),
    text_signature = "(path, size, data, block_size = (32, 32), /, shrink = false, shrinking_factor = 1., filter_type = 3)"
)]
fn save_image(
    path: &str,
    size: (u32, u32),
    data: &[u8],
    block_size: (u32, u32),
    shrink: bool,
    shrinking_factor: f32,
    filter_type: u8,
) -> PyResult<()> {
    let is_rgba = data.len() as u32 == size.0 * size.1 * 4;
    // Creates Pixlzr image
    let img = if is_rgba {
        let rgba = RgbaImage::from_raw(size.0, size.1, data.to_vec()).unwrap();
        DynamicImage::ImageRgba8(rgba)
    } else {
        let rgb = RgbImage::from_raw(size.0, size.1, data.to_vec()).unwrap();
        DynamicImage::ImageRgb8(rgb)
    };
    let mut img = Pixlzr::from_image(&img, block_size.0, block_size.1);
    // Saves encoded Pixlzr to file
    if shrink {
        img.shrink_by(filter_type.into(), shrinking_factor);
    }
    img.save(path)
        .map_err(|_| PyTypeError::new_err("Error saving."))?;

    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn pixlzr_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(decode_buffer_into_image, m)?)?;
    m.add_function(wrap_pyfunction!(encode_image, m)?)?;
    m.add_function(wrap_pyfunction!(open_image, m)?)?;
    m.add_function(wrap_pyfunction!(save_image, m)?)?;
    Ok(())
}
