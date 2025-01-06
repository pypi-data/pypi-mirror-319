# Generated by cloudcoil-model-codegen v0.0.24
# DO NOT EDIT

from __future__ import annotations

from typing import Annotated, Dict, List, Literal, Optional

from pydantic import Field

from cloudcoil import apimachinery
from cloudcoil._pydantic import BaseModel
from cloudcoil.resources import Resource, ResourceList


class CertificateSigningRequestSpec(BaseModel):
    expiration_seconds: Annotated[
        Optional[int],
        Field(
            alias="expirationSeconds",
            description="expirationSeconds is the requested duration of validity of the issued certificate. The certificate signer may issue a certificate with a different validity duration so a client must check the delta between the notBefore and and notAfter fields in the issued certificate to determine the actual duration.\n\nThe v1.22+ in-tree implementations of the well-known Kubernetes signers will honor this field as long as the requested duration is not greater than the maximum duration they will honor per the --cluster-signing-duration CLI flag to the Kubernetes controller manager.\n\nCertificate signers may not honor this field for various reasons:\n\n  1. Old signer that is unaware of the field (such as the in-tree\n     implementations prior to v1.22)\n  2. Signer whose configured maximum is shorter than the requested duration\n  3. Signer whose configured minimum is longer than the requested duration\n\nThe minimum valid value for expirationSeconds is 600, i.e. 10 minutes.",
        ),
    ] = None
    extra: Annotated[
        Optional[Dict[str, List[str]]],
        Field(
            description="extra contains extra attributes of the user that created the CertificateSigningRequest. Populated by the API server on creation and immutable."
        ),
    ] = None
    groups: Annotated[
        Optional[List[str]],
        Field(
            description="groups contains group membership of the user that created the CertificateSigningRequest. Populated by the API server on creation and immutable."
        ),
    ] = None
    request: Annotated[
        str,
        Field(
            description='request contains an x509 certificate signing request encoded in a "CERTIFICATE REQUEST" PEM block. When serialized as JSON or YAML, the data is additionally base64-encoded.'
        ),
    ]
    signer_name: Annotated[
        str,
        Field(
            alias="signerName",
            description='signerName indicates the requested signer, and is a qualified name.\n\nList/watch requests for CertificateSigningRequests can filter on this field using a "spec.signerName=NAME" fieldSelector.\n\nWell-known Kubernetes signers are:\n 1. "kubernetes.io/kube-apiserver-client": issues client certificates that can be used to authenticate to kube-apiserver.\n  Requests for this signer are never auto-approved by kube-controller-manager, can be issued by the "csrsigning" controller in kube-controller-manager.\n 2. "kubernetes.io/kube-apiserver-client-kubelet": issues client certificates that kubelets use to authenticate to kube-apiserver.\n  Requests for this signer can be auto-approved by the "csrapproving" controller in kube-controller-manager, and can be issued by the "csrsigning" controller in kube-controller-manager.\n 3. "kubernetes.io/kubelet-serving" issues serving certificates that kubelets use to serve TLS endpoints, which kube-apiserver can connect to securely.\n  Requests for this signer are never auto-approved by kube-controller-manager, and can be issued by the "csrsigning" controller in kube-controller-manager.\n\nMore details are available at https://k8s.io/docs/reference/access-authn-authz/certificate-signing-requests/#kubernetes-signers\n\nCustom signerNames can also be specified. The signer defines:\n 1. Trust distribution: how trust (CA bundles) are distributed.\n 2. Permitted subjects: and behavior when a disallowed subject is requested.\n 3. Required, permitted, or forbidden x509 extensions in the request (including whether subjectAltNames are allowed, which types, restrictions on allowed values) and behavior when a disallowed extension is requested.\n 4. Required, permitted, or forbidden key usages / extended key usages.\n 5. Expiration/certificate lifetime: whether it is fixed by the signer, configurable by the admin.\n 6. Whether or not requests for CA certificates are allowed.',
        ),
    ]
    uid: Annotated[
        Optional[str],
        Field(
            description="uid contains the uid of the user that created the CertificateSigningRequest. Populated by the API server on creation and immutable."
        ),
    ] = None
    usages: Annotated[
        Optional[List[str]],
        Field(
            description='usages specifies a set of key usages requested in the issued certificate.\n\nRequests for TLS client certificates typically request: "digital signature", "key encipherment", "client auth".\n\nRequests for TLS serving certificates typically request: "key encipherment", "digital signature", "server auth".\n\nValid values are:\n "signing", "digital signature", "content commitment",\n "key encipherment", "key agreement", "data encipherment",\n "cert sign", "crl sign", "encipher only", "decipher only", "any",\n "server auth", "client auth",\n "code signing", "email protection", "s/mime",\n "ipsec end system", "ipsec tunnel", "ipsec user",\n "timestamping", "ocsp signing", "microsoft sgc", "netscape sgc"'
        ),
    ] = None
    username: Annotated[
        Optional[str],
        Field(
            description="username contains the name of the user that created the CertificateSigningRequest. Populated by the API server on creation and immutable."
        ),
    ] = None


class CertificateSigningRequestCondition(BaseModel):
    last_transition_time: Annotated[
        Optional[apimachinery.Time],
        Field(
            alias="lastTransitionTime",
            description="lastTransitionTime is the time the condition last transitioned from one status to another. If unset, when a new condition type is added or an existing condition's status is changed, the server defaults this to the current time.",
        ),
    ] = None
    last_update_time: Annotated[
        Optional[apimachinery.Time],
        Field(
            alias="lastUpdateTime",
            description="lastUpdateTime is the time of the last update to this condition",
        ),
    ] = None
    message: Annotated[
        Optional[str],
        Field(
            description="message contains a human readable message with details about the request state"
        ),
    ] = None
    reason: Annotated[
        Optional[str],
        Field(description="reason indicates a brief reason for the request state"),
    ] = None
    status: Annotated[
        str,
        Field(
            description='status of the condition, one of True, False, Unknown. Approved, Denied, and Failed conditions may not be "False" or "Unknown".'
        ),
    ]
    type: Annotated[
        str,
        Field(
            description='type of the condition. Known conditions are "Approved", "Denied", and "Failed".\n\nAn "Approved" condition is added via the /approval subresource, indicating the request was approved and should be issued by the signer.\n\nA "Denied" condition is added via the /approval subresource, indicating the request was denied and should not be issued by the signer.\n\nA "Failed" condition is added via the /status subresource, indicating the signer failed to issue the certificate.\n\nApproved and Denied conditions are mutually exclusive. Approved, Denied, and Failed conditions cannot be removed once added.\n\nOnly one condition of a given type is allowed.'
        ),
    ]


class CertificateSigningRequestStatus(BaseModel):
    certificate: Annotated[
        Optional[str],
        Field(
            description='certificate is populated with an issued certificate by the signer after an Approved condition is present. This field is set via the /status subresource. Once populated, this field is immutable.\n\nIf the certificate signing request is denied, a condition of type "Denied" is added and this field remains empty. If the signer cannot issue the certificate, a condition of type "Failed" is added and this field remains empty.\n\nValidation requirements:\n 1. certificate must contain one or more PEM blocks.\n 2. All PEM blocks must have the "CERTIFICATE" label, contain no headers, and the encoded data\n  must be a BER-encoded ASN.1 Certificate structure as described in section 4 of RFC5280.\n 3. Non-PEM content may appear before or after the "CERTIFICATE" PEM blocks and is unvalidated,\n  to allow for explanatory text as described in section 5.2 of RFC7468.\n\nIf more than one PEM block is present, and the definition of the requested spec.signerName does not indicate otherwise, the first block is the issued certificate, and subsequent blocks should be treated as intermediate certificates and presented in TLS handshakes.\n\nThe certificate is encoded in PEM format.\n\nWhen serialized as JSON or YAML, the data is additionally base64-encoded, so it consists of:\n\n    base64(\n    -----BEGIN CERTIFICATE-----\n    ...\n    -----END CERTIFICATE-----\n    )'
        ),
    ] = None
    conditions: Annotated[
        Optional[List[CertificateSigningRequestCondition]],
        Field(
            description='conditions applied to the request. Known conditions are "Approved", "Denied", and "Failed".'
        ),
    ] = None


class CertificateSigningRequest(Resource):
    api_version: Annotated[
        Optional[Literal["certificates.k8s.io/v1"]],
        Field(
            alias="apiVersion",
            description="APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",
        ),
    ] = "certificates.k8s.io/v1"
    kind: Annotated[
        Optional[Literal["CertificateSigningRequest"]],
        Field(
            description="Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    ] = "CertificateSigningRequest"
    metadata: Optional[apimachinery.ObjectMeta] = None
    spec: Annotated[
        CertificateSigningRequestSpec,
        Field(
            description="spec contains the certificate request, and is immutable after creation. Only the request, signerName, expirationSeconds, and usages fields can be set on creation. Other fields are derived by Kubernetes and cannot be modified by users."
        ),
    ]
    status: Annotated[
        Optional[CertificateSigningRequestStatus],
        Field(
            description="status contains information about whether the request is approved or denied, and the certificate issued by the signer, or the failure condition indicating signer failure."
        ),
    ] = None


CertificateSigningRequestList = ResourceList["CertificateSigningRequest"]
