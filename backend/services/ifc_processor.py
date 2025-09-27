"""
IFC file processing service
"""

import os
import json
import logging
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal
from backend.models.ifc_file import IFCFile
from backend.models.ifc_space import IFCSpace

logger = logging.getLogger(__name__)


class IFCProcessor:
    """Service for processing IFC files"""
    
    def __init__(self):
        self.supported_versions = ["IFC2x3", "IFC4", "IFC4x1"]
    
    async def process_ifc_file(self, file_id: int, db: Session = None):
        """Process IFC file and extract building information"""
        if not db:
            db = SessionLocal()
        
        try:
            ifc_file = db.query(IFCFile).filter(IFCFile.id == file_id).first()
            if not ifc_file:
                raise ValueError(f"IFC file {file_id} not found")
            
            # Update processing status
            ifc_file.processing_status = "processing"
            db.commit()
            
            # Parse IFC file
            ifc_data = await self._parse_ifc_file(ifc_file.file_path)
            
            # Extract metadata
            metadata = await self._extract_metadata(ifc_data)
            
            # Update file metadata
            ifc_file.project_name = metadata.get("project_name")
            ifc_file.project_description = metadata.get("project_description")
            ifc_file.ifc_version = metadata.get("ifc_version")
            ifc_file.building_width = metadata.get("building_width")
            ifc_file.building_height = metadata.get("building_height")
            ifc_file.building_depth = metadata.get("building_depth")
            
            # Extract spaces
            spaces = await self._extract_spaces(ifc_data)
            
            # Save spaces to database
            for space_data in spaces:
                space = IFCSpace(
                    ifc_file_id=file_id,
                    ifc_id=space_data.get("ifc_id"),
                    name=space_data.get("name"),
                    long_name=space_data.get("long_name"),
                    description=space_data.get("description"),
                    space_type=space_data.get("space_type"),
                    usage_type=space_data.get("usage_type"),
                    area=space_data.get("area"),
                    volume=space_data.get("volume"),
                    height=space_data.get("height"),
                    x_coordinate=space_data.get("x_coordinate"),
                    y_coordinate=space_data.get("y_coordinate"),
                    z_coordinate=space_data.get("z_coordinate"),
                    level_name=space_data.get("level_name"),
                    level_elevation=space_data.get("level_elevation")
                )
                db.add(space)
            
            # Mark as processed
            ifc_file.processing_status = "completed"
            ifc_file.is_processed = True
            db.commit()
            
            logger.info(f"Successfully processed IFC file {file_id}")
            
        except Exception as e:
            logger.error(f"Error processing IFC file {file_id}: {str(e)}")
            ifc_file.processing_status = "failed"
            ifc_file.processing_error = str(e)
            db.commit()
            raise
        finally:
            if not db:
                db.close()
    
    async def _parse_ifc_file(self, file_path: str) -> Dict[str, Any]:
        """Parse IFC file and return structured data"""
        try:
            # This is a simplified IFC parser
            # In a real implementation, you would use a proper IFC library like ifcopenshell
            
            ifc_data = {
                "header": {},
                "entities": {},
                "spaces": [],
                "building_elements": []
            }
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Parse header
            ifc_data["header"] = await self._parse_header(content)
            
            # Extract basic entities (simplified parsing)
            ifc_data["entities"] = await self._parse_entities(content)
            
            # Extract spaces
            ifc_data["spaces"] = await self._extract_spaces_from_content(content)
            
            return ifc_data
            
        except Exception as e:
            logger.error(f"Error parsing IFC file {file_path}: {str(e)}")
            raise
    
    async def _parse_header(self, content: str) -> Dict[str, Any]:
        """Parse IFC file header"""
        header = {}
        
        lines = content.split('\n')
        in_header = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('HEADER'):
                in_header = True
                continue
            elif line.startswith('ENDSEC'):
                break
            elif in_header:
                # Parse header properties (simplified)
                if 'FILE_NAME' in line:
                    header['file_name'] = self._extract_value(line)
                elif 'FILE_DESCRIPTION' in line:
                    header['file_description'] = self._extract_value(line)
                elif 'FILE_SCHEMA' in line:
                    header['file_schema'] = self._extract_value(line)
        
        return header
    
    async def _parse_entities(self, content: str) -> Dict[str, Any]:
        """Parse IFC entities (simplified)"""
        entities = {}
        
        # This is a very simplified parser
        # Real IFC parsing would require a proper IFC library
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                # Extract entity ID and type
                parts = line.split('=')
                if len(parts) >= 2:
                    entity_id = parts[0].strip('#')
                    entity_def = parts[1].split('(')[0].strip()
                    entities[entity_id] = {
                        'type': entity_def,
                        'raw': line
                    }
        
        return entities
    
    async def _extract_spaces_from_content(self, content: str) -> List[Dict[str, Any]]:
        """Extract spaces from IFC content"""
        spaces = []
        
        # Find IFCSPACE entities
        lines = content.split('\n')
        for line in lines:
            if 'IFCSPACE' in line:
                space_data = await self._parse_space_entity(line)
                if space_data:
                    spaces.append(space_data)
        
        return spaces
    
    async def _parse_space_entity(self, line: str) -> Dict[str, Any]:
        """Parse individual IFCSPACE entity"""
        try:
            # This is a simplified parser
            # Extract basic information from IFCSPACE entity
            
            space_data = {
                'ifc_id': None,
                'name': None,
                'long_name': None,
                'description': None,
                'space_type': 'space',
                'usage_type': None,
                'area': None,
                'volume': None,
                'height': None,
                'x_coordinate': None,
                'y_coordinate': None,
                'z_coordinate': None,
                'level_name': None,
                'level_elevation': None
            }
            
            # Extract entity ID
            if line.startswith('#'):
                entity_id = line.split('=')[0].strip('#')
                space_data['ifc_id'] = entity_id
            
            # This is where you would implement proper IFC parsing
            # For now, we'll create some sample data
            
            return space_data
            
        except Exception as e:
            logger.error(f"Error parsing space entity: {str(e)}")
            return None
    
    async def _extract_metadata(self, ifc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract building metadata"""
        metadata = {}
        
        # Extract from header
        header = ifc_data.get("header", {})
        metadata["project_name"] = header.get("file_name", "Unknown Project")
        metadata["project_description"] = header.get("file_description", "")
        metadata["ifc_version"] = header.get("file_schema", "Unknown")
        
        # Calculate building dimensions (simplified)
        spaces = ifc_data.get("spaces", [])
        if spaces:
            # This would be calculated from actual space coordinates
            metadata["building_width"] = 50.0  # meters
            metadata["building_height"] = 10.0  # meters
            metadata["building_depth"] = 30.0   # meters
        
        return metadata
    
    async def _extract_spaces(self, ifc_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and format space data"""
        spaces = []
        
        raw_spaces = ifc_data.get("spaces", [])
        
        for i, space in enumerate(raw_spaces):
            # Enhance space data with calculated values
            enhanced_space = space.copy()
            
            # Add calculated coordinates if not present
            if not enhanced_space.get("x_coordinate"):
                enhanced_space["x_coordinate"] = (i % 10) * 5.0  # Sample positioning
            if not enhanced_space.get("y_coordinate"):
                enhanced_space["y_coordinate"] = (i // 10) * 5.0
            if not enhanced_space.get("z_coordinate"):
                enhanced_space["z_coordinate"] = 0.0
            
            # Add calculated area if not present
            if not enhanced_space.get("area"):
                enhanced_space["area"] = 25.0  # Sample area
            
            # Add name if not present
            if not enhanced_space.get("name"):
                enhanced_space["name"] = f"Space {i+1}"
            
            spaces.append(enhanced_space)
        
        return spaces
    
    def _extract_value(self, line: str) -> str:
        """Extract value from IFC property line"""
        try:
            # Simple value extraction (would need more sophisticated parsing)
            if '(' in line and ')' in line:
                start = line.find('(') + 1
                end = line.rfind(')')
                return line[start:end].strip("'\"")
            return ""
        except:
            return ""
