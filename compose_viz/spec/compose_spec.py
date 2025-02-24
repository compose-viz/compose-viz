# generated by datamodel-codegen:
#   filename:  compose-spec.json
#   timestamp: 2024-10-14T09:11:40+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel


class Cgroup(Enum):
    host = "host"
    private = "private"


class CredentialSpec(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    config: Optional[str] = None
    file: Optional[str] = None
    registry: Optional[str] = None


class Condition(Enum):
    service_started = "service_started"
    service_healthy = "service_healthy"
    service_completed_successfully = "service_completed_successfully"


class DependsOn(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    restart: Optional[bool] = None
    required: Optional[bool] = True
    condition: Condition


class Extends(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    service: str
    file: Optional[str] = None


class Logging(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    driver: Optional[str] = None
    options: Optional[Dict[str, Optional[Union[str, float]]]] = None


class Ports(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: Optional[str] = None
    mode: Optional[str] = None
    host_ip: Optional[str] = None
    target: Optional[int] = None
    published: Optional[Union[str, int]] = None
    protocol: Optional[str] = None
    app_protocol: Optional[str] = None


class PullPolicy(Enum):
    always = "always"
    never = "never"
    if_not_present = "if_not_present"
    build = "build"
    missing = "missing"


class Selinux(Enum):
    z = "z"
    Z = "Z"


class Bind(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    propagation: Optional[str] = None
    create_host_path: Optional[bool] = None
    selinux: Optional[Selinux] = None


class AdditionalVolumeOption(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    nocopy: Optional[bool] = None
    subpath: Optional[str] = None


class Size(RootModel[int]):
    root: int = Field(..., ge=0)


class Tmpfs(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    size: Optional[Union[Size, str]] = None
    mode: Optional[float] = None


class Volumes(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    type: str
    source: Optional[str] = None
    target: Optional[str] = None
    read_only: Optional[bool] = None
    consistency: Optional[str] = None
    bind: Optional[Bind] = None
    volume: Optional[AdditionalVolumeOption] = None
    tmpfs: Optional[Tmpfs] = None


class Healthcheck(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    disable: Optional[bool] = None
    interval: Optional[str] = None
    retries: Optional[float] = None
    test: Optional[Union[str, List[str]]] = None
    timeout: Optional[str] = None
    start_period: Optional[str] = None
    start_interval: Optional[str] = None


class Action(Enum):
    rebuild = "rebuild"
    sync = "sync"
    sync_restart = "sync+restart"


class WatchItem(BaseModel):
    ignore: Optional[List[str]] = None
    path: str
    action: Action
    target: Optional[str] = None


class Development(BaseModel):
    watch: Optional[List[WatchItem]] = None


class Order(Enum):
    start_first = "start-first"
    stop_first = "stop-first"


class RollbackConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    parallelism: Optional[int] = None
    delay: Optional[str] = None
    failure_action: Optional[str] = None
    monitor: Optional[str] = None
    max_failure_ratio: Optional[float] = None
    order: Optional[Order] = None


class UpdateConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    parallelism: Optional[int] = None
    delay: Optional[str] = None
    failure_action: Optional[str] = None
    monitor: Optional[str] = None
    max_failure_ratio: Optional[float] = None
    order: Optional[Order] = None


class Limits(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cpus: Optional[Union[float, str]] = None
    memory: Optional[str] = None
    pids: Optional[int] = None


class RestartPolicy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    condition: Optional[str] = None
    delay: Optional[str] = None
    max_attempts: Optional[int] = None
    window: Optional[str] = None


class Preference(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    spread: Optional[str] = None


class Placement(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    constraints: Optional[List[str]] = None
    preferences: Optional[List[Preference]] = None
    max_replicas_per_node: Optional[int] = None


class DiscreteResourceSpec(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    kind: Optional[str] = None
    value: Optional[float] = None


class GenericResource(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    discrete_resource_spec: Optional[DiscreteResourceSpec] = None


class GenericResources(RootModel[List[GenericResource]]):
    root: List[GenericResource]


class ConfigItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    subnet: Optional[str] = None
    ip_range: Optional[str] = None
    gateway: Optional[str] = None
    aux_addresses: Optional[Dict[str, str]] = None


class Ipam(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    driver: Optional[str] = None
    config: Optional[List[ConfigItem]] = None
    options: Optional[Dict[str, str]] = None


class ExternalVolumeNetwork(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: Optional[str] = None


class ExternalConfig(BaseModel):
    name: Optional[str] = None


class Command(RootModel[Optional[Union[str, List[str]]]]):
    root: Optional[Union[str, List[str]]]


class EnvFilePath(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    path: str
    required: Optional[bool] = True


class EnvFile(RootModel[Union[str, List[Union[str, EnvFilePath]]]]):
    root: Union[str, List[Union[str, EnvFilePath]]]


class ListOfStrings(RootModel[List[str]]):
    root: List[str]


class ListOrDict1(RootModel[List[Any]]):
    root: List[Any]


class ListOrDict(RootModel[Union[Dict[str, Optional[Union[str, float, bool]]], ListOrDict1]]):
    root: Union[Dict[str, Optional[Union[str, float, bool]]], ListOrDict1]


class BlkioLimit(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    path: Optional[str] = None
    rate: Optional[Union[int, str]] = None


class BlkioWeight(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    path: Optional[str] = None
    weight: Optional[int] = None


class ServiceConfigOrSecret1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    source: Optional[str] = None
    target: Optional[str] = None
    uid: Optional[str] = None
    gid: Optional[str] = None
    mode: Optional[float] = None


class ServiceConfigOrSecret(RootModel[List[Union[str, ServiceConfigOrSecret1]]]):
    root: List[Union[str, ServiceConfigOrSecret1]]


class Ulimits1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    hard: int
    soft: int


class Ulimits(RootModel[Dict[str, Union[int, Ulimits1]]]):
    root: Dict[str, Union[int, Ulimits1]]


class Constraints(RootModel[Any]):
    root: Any


class Build(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    context: Optional[str] = None
    dockerfile: Optional[str] = None
    dockerfile_inline: Optional[str] = None
    entitlements: Optional[List[str]] = None
    args: Optional[ListOrDict] = None
    ssh: Optional[ListOrDict] = None
    labels: Optional[ListOrDict] = None
    cache_from: Optional[List[str]] = None
    cache_to: Optional[List[str]] = None
    no_cache: Optional[bool] = None
    additional_contexts: Optional[ListOrDict] = None
    network: Optional[str] = None
    pull: Optional[bool] = None
    target: Optional[str] = None
    shm_size: Optional[Union[int, str]] = None
    extra_hosts: Optional[ListOrDict] = None
    isolation: Optional[str] = None
    privileged: Optional[bool] = None
    secrets: Optional[ServiceConfigOrSecret] = None
    tags: Optional[List[str]] = None
    ulimits: Optional[Ulimits] = None
    platforms: Optional[List[str]] = None


class BlkioConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    device_read_bps: Optional[List[BlkioLimit]] = None
    device_read_iops: Optional[List[BlkioLimit]] = None
    device_write_bps: Optional[List[BlkioLimit]] = None
    device_write_iops: Optional[List[BlkioLimit]] = None
    weight: Optional[int] = None
    weight_device: Optional[List[BlkioWeight]] = None


class Networks(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    aliases: Optional[ListOfStrings] = None
    ipv4_address: Optional[str] = None
    ipv6_address: Optional[str] = None
    link_local_ips: Optional[ListOfStrings] = None
    mac_address: Optional[str] = None
    driver_opts: Optional[Dict[str, Union[str, float]]] = None
    priority: Optional[float] = None


class Device(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    capabilities: Optional[ListOfStrings] = None
    count: Optional[Union[str, int]] = None
    device_ids: Optional[ListOfStrings] = None
    driver: Optional[str] = None
    options: Optional[ListOrDict] = None


class Devices(RootModel[List[Device]]):
    root: List[Device]


class Network(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: Optional[str] = None
    driver: Optional[str] = None
    driver_opts: Optional[Dict[str, Union[str, float]]] = None
    ipam: Optional[Ipam] = None
    external: Optional[Union[bool, ExternalVolumeNetwork]] = None
    internal: Optional[bool] = None
    enable_ipv6: Optional[bool] = None
    attachable: Optional[bool] = None
    labels: Optional[ListOrDict] = None


class Volume(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: Optional[str] = None
    driver: Optional[str] = None
    driver_opts: Optional[Dict[str, Union[str, float]]] = None
    external: Optional[Union[bool, ExternalVolumeNetwork]] = None
    labels: Optional[ListOrDict] = None


class Secret(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: Optional[str] = None
    environment: Optional[str] = None
    file: Optional[str] = None
    external: Optional[Union[bool, ExternalConfig]] = None
    labels: Optional[ListOrDict] = None
    driver: Optional[str] = None
    driver_opts: Optional[Dict[str, Union[str, float]]] = None
    template_driver: Optional[str] = None


class Config(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: Optional[str] = None
    content: Optional[str] = None
    environment: Optional[str] = None
    file: Optional[str] = None
    external: Optional[Union[bool, ExternalConfig]] = None
    labels: Optional[ListOrDict] = None
    template_driver: Optional[str] = None


class StringOrList(RootModel[Union[str, ListOfStrings]]):
    root: Union[str, ListOfStrings]


class Reservations(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    cpus: Optional[Union[float, str]] = None
    memory: Optional[str] = None
    generic_resources: Optional[GenericResources] = None
    devices: Optional[Devices] = None


class Resources(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    limits: Optional[Limits] = None
    reservations: Optional[Reservations] = None


class Deployment(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    mode: Optional[str] = None
    endpoint_mode: Optional[str] = None
    replicas: Optional[int] = None
    labels: Optional[ListOrDict] = None
    rollback_config: Optional[RollbackConfig] = None
    update_config: Optional[UpdateConfig] = None
    resources: Optional[Resources] = None
    restart_policy: Optional[RestartPolicy] = None
    placement: Optional[Placement] = None


class Include1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    path: Optional[StringOrList] = None
    env_file: Optional[StringOrList] = None
    project_directory: Optional[str] = None


class Include(RootModel[Union[str, Include1]]):
    root: Union[str, Include1]


class Service(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    develop: Optional[Development] = None
    deploy: Optional[Deployment] = None
    annotations: Optional[ListOrDict] = None
    attach: Optional[bool] = None
    build: Optional[Union[str, Build]] = None
    blkio_config: Optional[BlkioConfig] = None
    cap_add: Optional[List[str]] = None
    cap_drop: Optional[List[str]] = None
    cgroup: Optional[Cgroup] = None
    cgroup_parent: Optional[str] = None
    command: Optional[Command] = None
    configs: Optional[ServiceConfigOrSecret] = None
    container_name: Optional[str] = None
    cpu_count: Optional[int] = Field(None, ge=0)
    cpu_percent: Optional[int] = Field(None, ge=0, le=100)
    cpu_shares: Optional[Union[float, str]] = None
    cpu_quota: Optional[Union[float, str]] = None
    cpu_period: Optional[Union[float, str]] = None
    cpu_rt_period: Optional[Union[float, str]] = None
    cpu_rt_runtime: Optional[Union[float, str]] = None
    cpus: Optional[Union[float, str]] = None
    cpuset: Optional[str] = None
    credential_spec: Optional[CredentialSpec] = None
    depends_on: Optional[Union[ListOfStrings, Dict[str, DependsOn]]] = None
    device_cgroup_rules: Optional[ListOfStrings] = None
    devices: Optional[List[str]] = None
    dns: Optional[StringOrList] = None
    dns_opt: Optional[List[str]] = None
    dns_search: Optional[StringOrList] = None
    domainname: Optional[str] = None
    entrypoint: Optional[Command] = None
    env_file: Optional[EnvFile] = None
    environment: Optional[ListOrDict] = None
    expose: Optional[List[Union[str, float]]] = None
    extends: Optional[Union[str, Extends]] = None
    external_links: Optional[List[str]] = None
    extra_hosts: Optional[ListOrDict] = None
    group_add: Optional[List[Union[str, float]]] = None
    healthcheck: Optional[Healthcheck] = None
    hostname: Optional[str] = None
    image: Optional[str] = None
    init: Optional[bool] = None
    ipc: Optional[str] = None
    isolation: Optional[str] = None
    labels: Optional[ListOrDict] = None
    links: Optional[List[str]] = None
    logging: Optional[Logging] = None
    mac_address: Optional[str] = None
    mem_limit: Optional[Union[float, str]] = None
    mem_reservation: Optional[Union[str, int]] = None
    mem_swappiness: Optional[int] = None
    memswap_limit: Optional[Union[float, str]] = None
    network_mode: Optional[str] = None
    networks: Optional[Union[ListOfStrings, Dict[str, Optional[Networks]]]] = None
    oom_kill_disable: Optional[bool] = None
    oom_score_adj: Optional[int] = Field(None, ge=-1000, le=1000)
    pid: Optional[str] = None
    pids_limit: Optional[Union[float, str]] = None
    platform: Optional[str] = None
    ports: Optional[List[Union[float, str, Ports]]] = None
    privileged: Optional[bool] = None
    profiles: Optional[ListOfStrings] = None
    pull_policy: Optional[PullPolicy] = None
    read_only: Optional[bool] = None
    restart: Optional[str] = None
    runtime: Optional[str] = None
    scale: Optional[int] = None
    security_opt: Optional[List[str]] = None
    shm_size: Optional[Union[float, str]] = None
    secrets: Optional[ServiceConfigOrSecret] = None
    sysctls: Optional[ListOrDict] = None
    stdin_open: Optional[bool] = None
    stop_grace_period: Optional[str] = None
    stop_signal: Optional[str] = None
    storage_opt: Optional[Dict[str, Any]] = None
    tmpfs: Optional[StringOrList] = None
    tty: Optional[bool] = None
    ulimits: Optional[Ulimits] = None
    user: Optional[str] = None
    uts: Optional[str] = None
    userns_mode: Optional[str] = None
    volumes: Optional[List[Union[str, Volumes]]] = None
    volumes_from: Optional[List[str]] = None
    working_dir: Optional[str] = None


class ComposeSpecification(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    version: Optional[str] = Field(None, description="declared for backward compatibility, ignored.")
    name: Optional[str] = Field(
        None,
        description="define the Compose project name, until user defines one explicitly.",
        pattern="^[a-z0-9][a-z0-9_-]*$",
    )
    include: Optional[List[Include]] = Field(None, description="compose sub-projects to be included.")
    services: Optional[Dict[str, Service]] = None
    networks: Optional[Dict[str, Optional[Network]]] = None
    volumes: Optional[Dict[str, Optional[Volume]]] = None
    secrets: Optional[Dict[str, Secret]] = None
    configs: Optional[Dict[str, Config]] = None
