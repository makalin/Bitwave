use std::io::{Read, Write};
use std::path::Path;
use thiserror::Error;
use byteorder::{LittleEndian, ReadBytesExt, WriteBytesExt};
use serde::{Serialize, Deserialize};

/// Magic bytes for Bitwave files
const MAGIC_BYTES: &[u8] = b"BWX\0";

/// Version of the Bitwave format
const VERSION: u32 = 1;

/// Errors that can occur during Bitwave operations
#[derive(Error, Debug)]
pub enum BitwaveError {
    #[error("Invalid magic bytes")]
    InvalidMagicBytes,
    #[error("Unsupported version: {0}")]
    UnsupportedVersion(u32),
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[error("Invalid metadata")]
    InvalidMetadata,
}

/// Result type for Bitwave operations
pub type Result<T> = std::result::Result<T, BitwaveError>;

/// Metadata for a Bitwave file
#[derive(Debug, Serialize, Deserialize)]
pub struct Metadata {
    pub sample_rate: u32,
    pub channels: u16,
    pub duration: f64,
    pub bpm: Option<f32>,
}

/// Spatial data for a channel
#[derive(Debug, Serialize, Deserialize)]
pub struct SpatialData {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

/// Main Bitwave file structure
pub struct BitwaveFile {
    metadata: Metadata,
    spatial_data: Option<Vec<SpatialData>>,
    audio_data: Vec<u8>,
}

impl BitwaveFile {
    /// Create a new Bitwave file
    pub fn new(
        metadata: Metadata,
        spatial_data: Option<Vec<SpatialData>>,
        audio_data: Vec<u8>,
    ) -> Self {
        Self {
            metadata,
            spatial_data,
            audio_data,
        }
    }

    /// Read a Bitwave file from disk
    pub fn read<P: AsRef<Path>>(path: P) -> Result<Self> {
        let mut file = std::fs::File::open(path)?;
        Self::read_from(&mut file)
    }

    /// Read a Bitwave file from a reader
    pub fn read_from<R: Read>(reader: &mut R) -> Result<Self> {
        // Read and verify magic bytes
        let mut magic = [0u8; 4];
        reader.read_exact(&mut magic)?;
        if magic != MAGIC_BYTES {
            return Err(BitwaveError::InvalidMagicBytes);
        }

        // Read version
        let version = reader.read_u32::<LittleEndian>()?;
        if version != VERSION {
            return Err(BitwaveError::UnsupportedVersion(version));
        }

        // TODO: Implement reading metadata, spatial data, and audio data
        // This is a placeholder implementation
        Ok(Self {
            metadata: Metadata {
                sample_rate: 44100,
                channels: 2,
                duration: 0.0,
                bpm: None,
            },
            spatial_data: None,
            audio_data: Vec::new(),
        })
    }

    /// Write a Bitwave file to disk
    pub fn write<P: AsRef<Path>>(&self, path: P) -> Result<()> {
        let mut file = std::fs::File::create(path)?;
        self.write_to(&mut file)
    }

    /// Write a Bitwave file to a writer
    pub fn write_to<W: Write>(&self, writer: &mut W) -> Result<()> {
        // Write magic bytes
        writer.write_all(MAGIC_BYTES)?;

        // Write version
        writer.write_u32::<LittleEndian>(VERSION)?;

        // TODO: Implement writing metadata, spatial data, and audio data
        // This is a placeholder implementation
        Ok(())
    }

    /// Get the metadata
    pub fn metadata(&self) -> &Metadata {
        &self.metadata
    }

    /// Get the spatial data
    pub fn spatial_data(&self) -> Option<&Vec<SpatialData>> {
        self.spatial_data.as_ref()
    }

    /// Get the audio data
    pub fn audio_data(&self) -> &Vec<u8> {
        &self.audio_data
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::NamedTempFile;

    #[test]
    fn test_read_write() {
        let metadata = Metadata {
            sample_rate: 44100,
            channels: 2,
            duration: 0.0,
            bpm: Some(120.0),
        };

        let file = BitwaveFile::new(metadata, None, Vec::new());
        let temp_file = NamedTempFile::new().unwrap();
        let path = temp_file.path();

        file.write(path).unwrap();
        let read_file = BitwaveFile::read(path).unwrap();

        assert_eq!(read_file.metadata().sample_rate, 44100);
        assert_eq!(read_file.metadata().channels, 2);
    }
} 