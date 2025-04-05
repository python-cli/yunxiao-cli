from os.path import join
from typing import Tuple, List, Dict, Optional, Any, Union
import yaml
from yaml import Dumper, Loader

from ..sdk import OrganizationListAPI, ProjectListAPI
from ..model import ModelBase, Organization, Project, Member, Status
from .config import get_config_root, get_prefer_organization

def _setup_yaml_handlers():
    # Serialization: Convert ModelBase objects to YAML
    def model_base_representer(dumper: Dumper, obj: ModelBase) -> yaml.nodes.MappingNode:
        """Add a '__class__' field to track the object's type during serialization."""
        data = obj.dict.copy()
        data['__class__'] = obj.__class__.__name__  # Store class name
        return dumper.represent_mapping('!ModelBase', data)

    # Deserialization: Rebuild ModelBase objects from YAML
    def model_base_constructor(loader: Loader, node: yaml.nodes.MappingNode) -> ModelBase:
        """Use the '__class__' field to instantiate the correct subclass."""
        data = loader.construct_mapping(node)
        cls_name = data.pop('__class__')  # Extract class name
        cls = globals()[cls_name]         # Get the class from global scope
        return cls(**data)                # Rebuild the object

    # Register the custom handlers
    yaml.add_representer(ModelBase, model_base_representer)
    yaml.add_constructor('!ModelBase', model_base_constructor)

_setup_yaml_handlers()

def _get_config_file() -> str:
    return join(get_config_root(), 'cache.yaml')

def _save_to_cache(data: ModelBase) -> None:
    """Save a ModelBase object hierarchy to YAML."""
    with open(_get_config_file(), 'w') as f:
        yaml.dump(data, f, sort_keys=False)

def _load_from_cache() -> ModelBase:
    """Load a ModelBase object hierarchy from YAML."""
    with open(_get_config_file(), 'r') as f:
        return yaml.load(f, Loader=Loader)

def get_cached_organization(fetch: bool = False) -> Optional[Organization]:
    orgs = _load_from_cache()

    if fetch and not orgs:
        orgs = OrganizationListAPI.run()
        _save_to_cache(orgs)

        if not orgs:
            return None

    prefer_org_id = get_prefer_organization()

    if prefer_org_id:
        org = next((org for org in orgs if org.id == prefer_org_id))

        if org:
            return org

    return next((org for org in orgs if org.default == True), orgs[0])

def save_cached_organization(org: Organization):
    all_orgs = _load_from_cache()

    if all_orgs:
        # Filter out any existing org with same ID, then add the new one
        all_orgs = list(filter(lambda x: x != org, all_orgs))
        all_orgs.append(org)

        _save_to_cache(all_orgs)
    else:
        _save_to_cache([org])
