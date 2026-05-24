export {
  canonicalizeUrl,
} from "./canonicalize";
export {
  ConnectorInputError,
  NotImplementedError,
  type BytesInput,
  type Connector,
  type ConnectorInput,
  type FetchCtx,
  type GithubReleaseLike,
  type GithubReleasesInput,
  type HtmlInput,
} from "./contract";
export { contentHash, type ContentHashInput } from "./hash";
export {
  DuplicateConnectorError,
  getConnector,
  listRegisteredSourceTypes,
  registerConnector,
  UnknownSourceTypeError,
} from "./registry";
export * from "./types";

import "./connectors/rss";
import "./connectors/podcast-rss";
import "./connectors/article-url";
import "./connectors/github-releases";
import "./connectors/stubs";
