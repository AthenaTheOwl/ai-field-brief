import type { Connector } from "./contract";
import { SOURCE_TYPES, type SourceType } from "./types";

const connectors = new Map<SourceType, Connector<unknown>>();

export class UnknownSourceTypeError extends Error {
  public constructor(sourceType: string) {
    super(`unknown source type: ${sourceType}`);
    this.name = "UnknownSourceTypeError";
  }
}

export class DuplicateConnectorError extends Error {
  public constructor(sourceType: SourceType) {
    super(`connector already registered: ${sourceType}`);
    this.name = "DuplicateConnectorError";
  }
}

export function registerConnector<TConfig>(
  connector: Connector<TConfig>,
): void {
  if (connectors.has(connector.sourceType)) {
    throw new DuplicateConnectorError(connector.sourceType);
  }
  connectors.set(connector.sourceType, connector as Connector<unknown>);
}

export function getConnector(sourceType: SourceType): Connector<unknown> {
  const connector = connectors.get(sourceType);
  if (!connector) {
    throw new UnknownSourceTypeError(sourceType);
  }
  return connector;
}

export function listRegisteredSourceTypes(): SourceType[] {
  return SOURCE_TYPES.filter((sourceType) => connectors.has(sourceType));
}
