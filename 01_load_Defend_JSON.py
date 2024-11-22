import json
import requests

url_1 = 'https://d3fend.mitre.org/api/technique/all.json'
url_2 = 'https://d3fend.mitre.org/api/technique/'

char_count = 0

techniques = []

def write_defend_promts(technique, content):
    global char_count
    # hier koennte ihr promt stehen
    id = technique[4:-5]
    techniques.append(id)
    with open(f"output_defend/{id}.txt", "w") as f:
        f.write(content)
        f.close()
        print(f'Technique: {id}, was printed into: output/{id}.txt')
    char_count += len(content)

def pull_description(name):
    # name = d3f:ExceptionHandlerPointerValidation.json
    url_final = url_2 + name
    response = requests.get(url_final)
    data = response.json()

    text = data['description']['@graph']

    text = text[0]
    definition = text['d3f:definition']
    article = ''
    try:
        article = text['d3f:kb-article']
    except KeyError:
        article = ' '
    content = definition + article
    content = content.replace('\n', ' ')
    content = content.replace('*', 'OR')
    content = content.replace('## How it works', ' ')
    splitted_content = content.split('#')
    content = splitted_content[0]
    write_defend_promts(name, content)

    #print(article)
   # print(definition)

def pull_defend_ids():
    #api abfragen
    # Raus filern der Namen in eine Liste
    response = requests.get(url_1)
    data = response.json()

    text = data['@graph']

    for entry in text:
        name = entry['@id']
        name += '.json'
        # print(name)
        #name = d3f:URLAnalysis.json
        pull_description(name)

# extract_description('d3f:ExceptionHandlerPointerValidation.json')
# print(char_count)
# Create the DEFEND Files
# pull_defend_ids()
# Transform the File into Promts


# Show the total char count of the Promts
print(char_count)

# ca 168.719.000
total_chars = 168719
batch_pricing = round(total_chars/1000000)*0.25
print(f'Batch Pricing: {batch_pricing}$')
pricing = round(total_chars/1000000)*0.5
print(f'Normal API Pricing: {pricing}$')
print(techniques)

techniques_shortened = [
    "AccessModeling", "AccountLocking", "AdministrativeNetworkActivityAnalysis",
    "ApplicationConfigurationHardening", "AssetVulnerabilityEnumeration", "AuthenticationCacheInvalidation",
    "AuthenticationEventThresholding", "AuthorizationEventThresholding", "BiometricAuthentication",
    "BootloaderAuthentication", "BroadcastDomainIsolation", "ByteSequenceEmulation",
    "Certificate-basedAuthentication", "CertificateAnalysis", "CertificatePinning",
    "Client-serverPayloadProfiling", "ConfigurationInventory", "ConnectedHoneynet",
    "ConnectionAttemptAnalysis", "CredentialCompromiseScopeAnalysis", "CredentialRevoking",
    "CredentialRotation", "CredentialTransmissionScoping", "DNSAllowlisting",
    "DNSDenylisting", "DNSTrafficAnalysis", "DataExchangeMapping",
    "DataInventory", "DatabaseQueryStringAnalysis", "DeadCodeElimination",
    "DecoyFile", "DecoyNetworkResource", "DecoyPersona",
    "DecoyPublicRelease", "DecoySessionToken", "DecoyUserCredential",
    "DiskEncryption", "DomainAccountMonitoring", "DomainTrustPolicy",
    "DriverLoadIntegrityChecking", "DynamicAnalysis", "EmulatedFileAnalysis",
    "EncryptedTunnels", "ExceptionHandlerPointerValidation", "ExecutableAllowlisting",
    "ExecutableDenylisting", "FileAccessPatternAnalysis", "FileCarving",
    "FileEncryption", "FileHashing", "FileIntegrityMonitoring",
    "FileRemoval", "FirmwareBehaviorAnalysis", "FirmwareEmbeddedMonitoringCode",
    "FirmwareVerification", "Hardware-basedProcessIsolation", "HardwareComponentInventory",
    "HomoglyphDetection", "HostShutdown", "IOPortRestriction",
    "IPCTrafficAnalysis", "IdentifierActivityAnalysis", "IdentifierReputationAnalysis",
    "InboundSessionVolumeAnalysis", "IndirectBranchCallAnalysis", "IntegratedHoneynet",
    "JobFunctionAccessPatternAnalysis", "Kernel-basedProcessIsolation", "LocalAccountMonitoring",
    "LocalFilePermissions", "LogicalLinkMapping", "MessageAuthentication",
    "MessageEncryption", "Multi-factorAuthentication", "NetworkNodeInventory",
    "NetworkTrafficCommunityDeviation", "NetworkTrafficFiltering", "NetworkTrafficPolicyMapping",
    "NetworkTrafficSignatureAnalysis", "NetworkVulnerabilityAssessment", "One-timePassword",
    "OperatingSystemMonitoring", "OperationalDependencyMapping", "OperationalRiskAssessment",
    "OrganizationMapping", "PerHostDownload-UploadRatioAnalysis", "PhysicalLinkMapping",
    "PointerAuthentication", "ProcessCodeSegmentVerification", "ProcessSegmentExecutionPrevention",
    "ProcessSelf-ModificationDetection", "ProcessSpawnAnalysis", "ProcessSuspension",
    "ProcessTermination", "ProtocolMetadataAnomalyDetection", "RFShielding",
    "RPCTrafficAnalysis", "ReissueCredential", "RelayPatternAnalysis",
    "RemoteTerminalSessionDetection", "ResourceAccessPatternAnalysis", "RestoreConfiguration",
    "RestoreDatabase", "RestoreDiskImage", "RestoreFile",
    "RestoreNetworkAccess", "RestoreSoftware", "RestoreUserAccountAccess",
    "ScriptExecutionAnalysis", "SegmentAddressOffsetRandomization", "SenderMTAReputationAnalysis",
    "SenderReputationAnalysis", "ServiceDependencyMapping", "SessionDurationAnalysis",
    "ShadowStackComparisons", "SoftwareInventory", "SoftwareUpdate",
    "StackFrameCanaryValidation", "StandaloneHoneynet", "StrongPasswordPolicy",
    "SystemCallAnalysis", "SystemConfigurationPermissions", "SystemDependencyMapping",
    "SystemVulnerabilityAssessment", "TPMBootIntegrity", "TransferAgentAuthentication",
    "URLAnalysis", "UserAccountPermissions", "UserDataTransferAnalysis",
    "UserGeolocationLogonPatternAnalysis", "WebSessionActivityAnalysis"
]


for t in techniques_shortened:
    with open("output/techniques.txt", "a") as f:
        f.write(t)
        f.write("\n")