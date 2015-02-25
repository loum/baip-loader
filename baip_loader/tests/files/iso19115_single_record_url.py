ISO19115_ITEM_URL = {
    "@xsi:schemaLocation": "http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd http://www.opengis.net/gml http://www.isotc211.org/2005/gml/gml.xsd http://www.w3.org/1999/xlink http://www.isotc211.org/2005/xlink/xlinks.xsd", 
    "gmd:fileIdentifier": {
        "gco:CharacterString": "505E8A67-90B4-408A-AA0D-038A9FB14F42"
    }, 
    "gmd:language": {
        "gco:CharacterString": "eng"
    }, 
    "gmd:characterSet": {
        "gmd:MD_CharacterSetCode": {
            "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_CharacterSetCode", 
            "@codeListValue": "utf8", 
            "#text": "utf8"
        }
    }, 
    "gmd:hierarchyLevel": {
        "gmd:MD_ScopeCode": {
            "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/GAScopeCodeList.xml#MD_ScopeCode", 
            "@codeListValue": "dataset", 
            "#text": "dataset"
        }
    }, 
    "gmd:hierarchyLevelName": {
        "gco:CharacterString": None
    }, 
    "gmd:contact": {
        "gmd:CI_ResponsibleParty": {
            "gmd:individualName": {
                "@gco:nilReason": "withheld", 
                "gco:CharacterString": "Jill McNamara"
            }, 
            "gmd:organisationName": {
                "gco:CharacterString": "Bureau of Meteolorology"
            }, 
            "gmd:positionName": {
                "gco:CharacterString": None
            }, 
            "gmd:contactInfo": {
                "gmd:CI_Contact": {
                    "gmd:phone": {
                        "gmd:CI_Telephone": {
                            "gmd:voice": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:facsimile": {
                                "gco:CharacterString": None
                            }
                        }
                    }, 
                    "gmd:address": {
                        "gmd:CI_Address": {
                            "gmd:deliveryPoint": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:city": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:administrativeArea": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:postalCode": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:country": {
                                "gco:CharacterString": "Australia"
                            }, 
                            "gmd:electronicMailAddress": {
                                "gco:CharacterString": "j.mcnamara@bom.gov.au"
                            }
                        }
                    }
                }
            }, 
            "gmd:role": {
                "gmd:CI_RoleCode": {
                    "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_RoleCode", 
                    "@codeListValue": "pointOfContact", 
                    "#text": "pointOfContact"
                }
            }
        }
    }, 
    "gmd:dateStamp": {
        "gco:Date": "2015-02-17"
    }, 
    "gmd:metadataStandardName": {
        "gco:CharacterString": "ANZLIC Metadata Profile: An Australian/New Zealand Profile of AS/NZS ISO 19115:2005, Geographic information - Metadata"
    }, 
    "gmd:metadataStandardVersion": {
        "gco:CharacterString": "1.1"
    }, 
    "gmd:referenceSystemInfo": {
        "gmd:MD_ReferenceSystem": {
            "gmd:referenceSystemIdentifier": {
                "gmd:RS_Identifier": {
                    "gmd:code": {
                        "gco:CharacterString": "Geodetic Datum of Australian 1994"
                    }
                }
            }
        }
    }, 
    "gmd:identificationInfo": {
        "gmd:MD_DataIdentification": {
            "gmd:citation": {
                "gmd:CI_Citation": {
                    "gmd:title": {
                        "gco:CharacterString": "NSW Office of Water_GW licence extract linked to spatial locations_NIC_v2_28022014"
                    }, 
                    "gmd:alternateTitle": {
                        "gco:CharacterString": None
                    }, 
                    "gmd:date": [
                        {
                            "gmd:CI_Date": {
                                "gmd:date": {
                                    "gco:Date": "2015-02-17"
                                }, 
                                "gmd:dateType": {
                                    "gmd:CI_DateTypeCode": {
                                        "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_DateTypeCode", 
                                        "@codeListValue": "creation", 
                                        "#text": "creation"
                                    }
                                }
                            }
                        }, 
                        {
                            "gmd:CI_Date": {
                                "gmd:date": {
                                    "gco:Date": "2014-02-28"
                                }, 
                                "gmd:dateType": {
                                    "gmd:CI_DateTypeCode": {
                                        "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_DateTypeCode", 
                                        "@codeListValue": "publication", 
                                        "#text": "publication"
                                    }
                                }
                            }
                        }, 
                        {
                            "gmd:CI_Date": {
                                "gmd:date": {
                                    "gco:Date": "2015-02-17"
                                }, 
                                "gmd:dateType": {
                                    "gmd:CI_DateTypeCode": {
                                        "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_DateTypeCode", 
                                        "@codeListValue": "revision", 
                                        "#text": "revision"
                                    }
                                }
                            }
                        }
                    ], 
                    "gmd:otherCitationDetails": {
                        "gco:CharacterString": None
                    }
                }
            }, 
            "gmd:abstract": {
                "gco:CharacterString": """The aim of this dataset was to be able to map each groundwater works with the volumetric entitlement without double counting the volume and to aggregate/ disaggregate the data depending on the final use.

This has not been clipped to the NIC PAE, therefore the number of economic assets/ relevant licences will drastically reduce once this occurs. 

The Northern_Inland_Catchment groundwater licences includes an extract of all licences that fell within the data management acquisition area as provided by BA to NSW Office of Water.



Aim: To get a one to one ratio of licences numbers to bore IDs. 
Important notes about data:
Data has not been clipped to the PAE.

No decision have been made in regards to what purpose of groundwater should be protected. Therefore the purpose currently includes groundwater bores that have been drilled for non-extractive purposes including experimental research, test, monitoring bore, teaching, mineral explore and groundwater explore
No volume has been included for domestic & stock as it is a basic right. Therefore an arbitrary volume could be applied to account for D&S use.
Licence Number - Each sheet in the Original Data has a licence number, this is assumed to be the actual licence number. Some are old  because they have not been updated to the new WA. Some are new (From_Spreadsheet_WALs). This is the reason for the different codes.
WA/CA - This number is the \'works\' number. It is assumed that the number indicates the bore permit or works approval. This is why there can be multiple works to licence and licences to works number. (For complete glossary see here http://registers.water.nsw.gov.au/wma/Glossary.jsp). Originally, the aim was to make sure that the when there was more than more than one licence to works number or mulitple works to licenes that the mulitple instances were compelte. 

Northern_Inland_Catchement worksheet links the individual licence to a works and a volumetric entitlement. For most sites, this can be linked to a bore which can be found in the NGIS through the HydroID. (\\\\\\\\wron\\\\Project\\\\BA\\\\BA_all\\\\Hydrogeology\\\\_National_Groundwater_Information_System_v1.1_Sept2013). This will allow analysis of depths, lithology and hydrostratigraphy where the data exists.
We can aggregate the data based on water source and water management zone as can be seen in the other worksheets. 



Data available: 

Original Data: Any data that was bought in from NSW Offcie of Water, includes
Spatial locations provided by NoW- This is a exported data from the submitted shape files. Includes the licence (LICENCE) numbers and the bore ID (WORK_NUO). (Refer to lineage NSW Office of Water Groundwater Entitlements Spatial Locations).
Spreadsheet_WAL - The spread sheet from the submitted data, _WLS-EXTRACT_3_WALs_volume. (Refer to Lineage NSW Office of Water Groundwater Licence Extract NIC- Oct 2013)
WLS_extracts - The combined spread sheets from the submitted data, _WLS-EXTRACT.  (Refer to Lineage NSW Office of Water Groundwater Licence Extract NIC- Oct 2013)

Processed Data: The two final products, includes
NIC_Draft - this includes cancelled licences and licences where the old licence has been replaced by a share component (essentially a repeat)
NIC_final- The final working linking all licences to bore IDs, removal of cancelled licences and licences that have been replaced in the new WaterAct. Also includes the volume of the licence per works 
Aggregated share component to water sharing plan, water source and water management zone"""
            }, 
            "gmd:purpose": {
                "gco:CharacterString": None
            }, 
            "gmd:status": {
                "gmd:MD_ProgressCode": {
                    "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_ProgressCode", 
                    "@codeListValue": "completed", 
                    "#text": "completed"
                }
            }, 
            "gmd:descriptiveKeywords": [
                {
                    "gmd:MD_Keywords": {
                        "gmd:keyword": {
                            "gco:CharacterString": "New South Wales"
                        }, 
                        "gmd:type": {
                            "gmd:MD_KeywordTypeCode": {
                                "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_KeywordTypeCode", 
                                "@codeListValue": "theme", 
                                "#text": "theme"
                            }
                        }, 
                        "gmd:thesaurusName": {
                            "gmd:CI_Citation": {
                                "gmd:title": {
                                    "gco:CharacterString": "ANZLIC Jurisdictions"
                                }, 
                                "gmd:date": {
                                    "gmd:CI_Date": {
                                        "gmd:date": {
                                            "gco:Date": "2015-02-17"
                                        }, 
                                        "gmd:dateType": {
                                            "gmd:CI_DateTypeCode": {
                                                "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_DateTypeCode", 
                                                "@codeListValue": "revision", 
                                                "#text": "revision"
                                            }
                                        }
                                    }
                                }, 
                                "gmd:edition": {
                                    "gco:CharacterString": "Version 2.1"
                                }, 
                                "gmd:editionDate": {
                                    "gco:Date": "2015-02-17"
                                }, 
                                "gmd:identifier": {
                                    "gmd:MD_Identifier": {
                                        "gmd:code": {
                                            "gco:CharacterString": "http://asdd.ga.gov.au/asdd/profileinfo/anzlic-jurisdic.xml#anzlic-jurisdic"
                                        }
                                    }
                                }, 
                                "gmd:citedResponsibleParty": {
                                    "gmd:CI_ResponsibleParty": {
                                        "gmd:organisationName": {
                                            "gco:CharacterString": "ANZLIC the Spatial Information Council"
                                        }, 
                                        "gmd:role": {
                                            "gmd:CI_RoleCode": {
                                                "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_RoleCode", 
                                                "@codeListValue": "custodian", 
                                                "#text": "custodian"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }, 
                None
            ], 
            "gmd:resourceConstraints": [
                None, 
                {
                    "gmd:MD_LegalConstraints": {
                        "gmd:useLimitation": {
                            "gco:CharacterString": """This data was given to the Bureau with a Creative Commons Attribution (CCBY). The license conditions allow publication of the data in a Bioregional Assessment product, provided NoW is attributed as the owner. NOW should be attributed as follows:

\\u00c2\\u00a9 State of NSW (NSW Office of Water)
1. this data could be made available to government agencies and/or consultants acting for government agencies for use in research/models/etc
2. a caveat to their use of the data was that no individual data could be published
3. data could be published if rolled up to a level (possibly water source) such that an individual\'s data could not be discerned"""
                        }, 
                        "gmd:useConstraints": {
                            "gmd:MD_RestrictionCode": {
                                "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_RestrictionCode", 
                                "@codeListValue": "licence", 
                                "#text": "licence"
                            }
                        }
                    }
                }
            ], 
            "gmd:language": {
                "gco:CharacterString": "eng"
            }, 
            "gmd:characterSet": {
                "gmd:MD_CharacterSetCode": {
                    "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_CharacterSetCode", 
                    "@codeListValue": "utf8", 
                    "#text": "utf8"
                }
            }, 
            "gmd:topicCategory": [
                {
                    "gmd:MD_TopicCategoryCode": "environment"
                }, 
                {
                    "gmd:MD_TopicCategoryCode": "geoscientificInformation"
                }
            ], 
            "gmd:extent": [
                {
                    "gmd:EX_Extent": {
                        "gmd:geographicElement": {
                            "gmd:EX_GeographicBoundingBox": {
                                "gmd:westBoundLongitude": {
                                    "gco:Decimal": "0"
                                }, 
                                "gmd:eastBoundLongitude": {
                                    "gco:Decimal": "0"
                                }, 
                                "gmd:southBoundLatitude": {
                                    "gco:Decimal": "0"
                                }, 
                                "gmd:northBoundLatitude": {
                                    "gco:Decimal": "0"
                                }
                            }
                        }
                    }
                }, 
                {
                    "gmd:EX_Extent": {
                        "gmd:geographicElement": {
                            "gmd:EX_GeographicDescription": {
                                "gmd:geographicIdentifier": {
                                    "gmd:MD_Identifier": {
                                        "gmd:authority": {
                                            "gmd:CI_Citation": {
                                                "gmd:title": {
                                                    "gco:CharacterString": "ANZLIC Geographic Extent Name Register"
                                                }, 
                                                "gmd:date": {
                                                    "gmd:CI_Date": {
                                                        "gmd:date": {
                                                            "gco:Date": "2006-10-10"
                                                        }, 
                                                        "gmd:dateType": {
                                                            "gmd:CI_DateTypeCode": {
                                                                "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_DateTypeCode", 
                                                                "@codeListValue": "publication", 
                                                                "#text": "publication"
                                                            }
                                                        }
                                                    }
                                                }, 
                                                "gmd:edition": {
                                                    "gco:CharacterString": "Version 2"
                                                }, 
                                                "gmd:editionDate": {
                                                    "gco:Date": "2001-02-01"
                                                }, 
                                                "gmd:identifier": {
                                                    "gmd:MD_Identifier": {
                                                        "gmd:code": {
                                                            "gco:CharacterString": "http://asdd.ga.gov.au/asdd/profileinfo/anzlic-allgens.xml#anzlic-state_territory"
                                                        }
                                                    }
                                                }, 
                                                "gmd:citedResponsibleParty": {
                                                    "gmd:CI_ResponsibleParty": {
                                                        "gmd:organisationName": {
                                                            "gco:CharacterString": "ANZLIC the Spatial Information Council"
                                                        }, 
                                                        "gmd:role": {
                                                            "gmd:CI_RoleCode": {
                                                                "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_RoleCode", 
                                                                "@codeListValue": "custodian", 
                                                                "#text": "custodian"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }, 
                                        "gmd:code": {
                                            "gco:CharacterString": "NSW"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        }
    }, 
    "gmd:distributionInfo": {
        "gmd:MD_Distribution": {
            "gmd:distributor": {
                "gmd:MD_Distributor": {
                    "gmd:distributorContact": {
                        "gmd:CI_ResponsibleParty": {
                            "gmd:individualName": {
                                "gco:CharacterString": "Jill McNamara"
                            }, 
                            "gmd:organisationName": {
                                "gco:CharacterString": "Bureau of Meteorology, Climate and Water Division"
                            }, 
                            "gmd:positionName": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:contactInfo": {
                                "gmd:CI_Contact": {
                                    "gmd:phone": {
                                        "gmd:CI_Telephone": {
                                            "gmd:voice": {
                                                "gco:CharacterString": "0396168453"
                                            }, 
                                            "gmd:facsimile": {
                                                "gco:CharacterString": None
                                            }
                                        }
                                    }, 
                                    "gmd:address": {
                                        "gmd:CI_Address": {
                                            "gmd:deliveryPoint": {
                                                "gco:CharacterString": None
                                            }, 
                                            "gmd:city": {
                                                "gco:CharacterString": None
                                            }, 
                                            "gmd:administrativeArea": {
                                                "gco:CharacterString": None
                                            }, 
                                            "gmd:postalCode": {
                                                "gco:CharacterString": None
                                            }, 
                                            "gmd:country": {
                                                "gco:CharacterString": "Australia"
                                            }, 
                                            "gmd:electronicMailAddress": {
                                                "gco:CharacterString": "j.mcnamara@bom.gov.au"
                                            }
                                        }
                                    }
                                }
                            }, 
                            "gmd:role": {
                                "gmd:CI_RoleCode": {
                                    "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_RoleCode", 
                                    "@codeListValue": "pointOfContact", 
                                    "#text": "pointOfContact"
                                }
                            }
                        }
                    }, 
                    "gmd:distributionOrderProcess": {
                        "gmd:MD_StandardOrderProcess": {
                            "gmd:fees": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:plannedAvailableDateTime": {
                                "gco:DateTime": "2015-02-17T16:19:21"
                            }, 
                            "gmd:orderingInstructions": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:turnaround": {
                                "gco:CharacterString": None
                            }
                        }
                    }, 
                    "gmd:distributorFormat": {
                        "gmd:MD_Format": {
                            "gmd:name": {
                                "gco:CharacterString": "n/a"
                            }, 
                            "gmd:version": {
                                "gco:CharacterString": "n/a"
                            }, 
                            "gmd:amendmentNumber": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:specification": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:fileDecompressionTechnique": {
                                "gco:CharacterString": None
                            }
                        }
                    }, 
                    "gmd:distributorTransferOptions": {
                        "gmd:MD_DigitalTransferOptions": {
                            "gmd:unitsOfDistribution": {
                                "gco:CharacterString": None
                            }, 
                            "gmd:transferSize": {
                                "gco:Real": "0.00"
                            }, 
                            "gmd:onLine": {
                                "gmd:CI_OnlineResource": {
                                    "gmd:linkage": {
                                        "gmd:URL": "n/a"
                                    }, 
                                    "gmd:protocol": {
                                        "gco:CharacterString": None
                                    }, 
                                    "gmd:applicationProfile": {
                                        "gco:CharacterString": None
                                    }, 
                                    "gmd:name": {
                                        "gco:CharacterString": None
                                    }, 
                                    "gmd:description": {
                                        "gco:CharacterString": None
                                    }, 
                                    "gmd:function": None
                                }
                            }, 
                            "gmd:offLine": {
                                "gmd:MD_Medium": {
                                    "gmd:name": None, 
                                    "gmd:density": {
                                        "gco:Real": "0.00"
                                    }, 
                                    "gmd:densityUnits": {
                                        "gco:CharacterString": None
                                    }, 
                                    "gmd:volumes": {
                                        "gco:Integer": "0"
                                    }, 
                                    "gmd:mediumNote": {
                                        "gco:CharacterString": None
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }, 
    "gmd:dataQualityInfo": {
        "gmd:DQ_DataQuality": {
            "gmd:scope": {
                "gmd:DQ_Scope": {
                    "gmd:level": {
                        "gmd:MD_ScopeCode": {
                            "@codeList": "http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_ScopeCode", 
                            "@codeListValue": "series", 
                            "#text": "series"
                        }
                    }, 
                    "gmd:levelDescription": {
                        "gmd:MD_ScopeDescription": {
                            "gmd:other": {
                                "gco:CharacterString": "series"
                            }
                        }
                    }
                }
            }, 
            "gmd:lineage": {
                "gmd:LI_Lineage": {
                    "gmd:statement": {
                        "gco:CharacterString": """Instructions


Procedure: refer to  Bioregional assessment data conversion script.docx

1) Original spread sheets have mulitple licence instances if there are more than one WA/CA number. This means that there are mpre than one works or permit to the licence. The aim is to only have one licence instance. 

2) The individual licence numbers were combined into one column 

3) Using the new column of licence numbers, several vlookups were created to bring in other data. Where the columns are identical in the original spreadsheets, they are combined. The only ones that dont are the Share/Entitlement/allocation, these mean different things. 

4) A hydro ID column was created, this is a code that links this NSW to the NGIS, which is basically a \\".1.1\\" at the end of the bore code.

5) All \'cancelled\' licences were removed

6) A count of the number of works per licence and number of bores were included in the spreadsheet.

7) Where the ShareComponent = NA, the Entitlement = 0, Allocation = 0 and there was more than one instance of the same bore, this means that the original licence assigned to the bore has been replaced by a new licence with a share component. Where these criteria were met, the instances were removed

8) a volume per works ensures that the volume of the licence is not repeated for each works, but is divided by the number of works


Bioregional assessment data conversion script

Aim: The following document is the R-Studio script for the conversion and merging of the bioregional assessment data. 

Requirements: The user will need R-Studio. It would be recommended that there is some basic knowledge of R. If there isn\\u00e2\\u0080\\u0099t, the only thing that would really need to be changed is the file location and name. The way that R reads files is different to windows and also the locations that R-Studio read is dependent on where R-Studio is originally installed to point. This would need to be completed properly before the script can be run. 

Procedure: The information below the dashed line is the script. This can be copied and pasted directly into R-Studio. Any text with \\u00e2\\u0080\\u0098#\\u00e2\\u0080\\u0099 will not be read as a script, so that can be added in and read as an instruction.

--------------------------------------------------------------------------------------------------------------------------------------

###########
# 18/2/2014
# Code by Brendan Dimech
#
# Script to merge extract files from submitted NSW bioregional 
# assessment and convert data into required format. Also use a \'vlookup\' 
# process to get Bore and Location information from NGIS.
#
# There are 3 scripts, one for each of the individual regions. 
# 
############
#North Inland

# Opening of files. Location can be changed if needed. 

# arc.file is the exported *.csv from the NGIS data which has bore data and Lat/long information. 
# Lat/long werent in the file nativly so were added to the table using Arc Toolbox tools.

arc.folder = \'/data/cdc_cwd_wra/awra/wra_share_01/GW_licencing_and_use_data/Rstudio/Data/Vlookup/Data\'
arc.file = \\"Arc_Northern_Inland.csv\\"

# Files from NSW came through in two types. WALS files, this included \'newer\' licences that had a share componant.
# The \'OTH\' files were older licences that had just an allocation. Some data was similar and this was combined, 
# and other inforamtion that wasn\'t similar from the datasets was removed. 

# This section is locating and importing the WALS and OTH files.

WALS.folder = \'/data/cdc_cwd_wra/awra/wra_share_01/GW_licencing_and_use_data/Rstudio/Data/Vlookup/Data\'

WALS.file.1 = \\"GW_Northern_Inland_Catchment_WLS-EXTRACT_1_WALs_volume.xls\\"
WALS.file.2 = \\"GW_Northern_Inland_Catchment_WLS-EXTRACT_2_WALs_volume.xls\\"
WALS.file.3 = \\"GW_Northern_Inland_Catchment_WLS-EXTRACT_3_WALs_volume.xls\\"
WALS.file.4 = \\"GW_Northern_Inland_Catchment_WLS-EXTRACT_4_WALs_volume.xls\\"
WALS.file.5 = \\"GW_Northern_Inland_Catchment_WLS-EXTRACT_5_WALs_volume.xls\\"

OTH.file.1 = \\"GW_Northern_Inland_Catchment_WLS-EXTRACT_1.xls\\"
OTH.file.2 = \\"GW_Northern_Inland_Catchment_WLS-EXTRACT_2.xls\\"
OTH.file.3 = \\"GW_Northern_Inland_Catchment_WLS-EXTRACT_3.xls\\"
OTH.file.4 = \\"GW_Northern_Inland_Catchment_WLS-EXTRACT_4.xls\\"
OTH.file.5 = \\"GW_Northern_Inland_Catchment_WLS-EXTRACT_5.xls\\"


newWALS.folder = \'/data/cdc_cwd_wra/awra/wra_share_01/GW_licencing_and_use_data/Rstudio/Data/Vlookup/Products\'
newWALS.file = \\"Northern_Inland_Catchment.csv\\"

arc <- read.csv(paste(arc.folder, arc.file, sep=\\"/\\" ), header =TRUE, sep = \\",\\")

# Merge any individual WALS and OTH files into a single WALS or OTH file if there were more than one.

WALS1 <- read.table(paste(WALS.folder, WALS.file.1, sep=\\"/\\" ), header =TRUE, sep = \\"\\\\t\\")
WALS2 <- read.table(paste(WALS.folder, WALS.file.2, sep=\\"/\\" ), header =TRUE, sep = \\"\\\\t\\")
WALS3 <- read.table(paste(WALS.folder, WALS.file.3, sep=\\"/\\" ), header =TRUE, sep = \\"\\\\t\\")
WALS4 <- read.table(paste(WALS.folder, WALS.file.4, sep=\\"/\\" ), header =TRUE, sep = \\"\\\\t\\")
WALS5 <- read.table(paste(WALS.folder, WALS.file.5, sep=\\"/\\" ), header =TRUE, sep = \\"\\\\t\\")


WALS <- merge(WALS1,WALS2, all.y = TRUE, all.x = TRUE)
WALS <- merge(WALS,WALS3, all.y = TRUE, all.x = TRUE)
WALS <- merge(WALS,WALS4, all.y = TRUE, all.x = TRUE)
WALS <- merge(WALS,WALS5, all.y = TRUE, all.x = TRUE)


#Merging OTHERS

OTH1 <- read.table(paste(WALS.folder, OTH.file.1, sep=\\"/\\" ), header =TRUE, sep = \\"\\\\t\\")
OTH2 <- read.table(paste(WALS.folder, OTH.file.2, sep=\\"/\\" ), header =TRUE, sep = \\"\\\\t\\")
OTH3 <- read.table(paste(WALS.folder, OTH.file.3, sep=\\"/\\" ), header =TRUE, sep = \\"\\\\t\\")
OTH4 <- read.table(paste(WALS.folder, OTH.file.4, sep=\\"/\\" ), header =TRUE, sep = \\"\\\\t\\")
OTH5 <- read.table(paste(WALS.folder, OTH.file.5, sep=\\"/\\" ), header =TRUE, sep = \\"\\\\t\\")

OTH <- merge(OTH1,OTH2, all.y = TRUE, all.x = TRUE)
OTH <- merge(OTH,OTH3, all.y = TRUE, all.x = TRUE)
OTH <- merge(OTH,OTH4, all.y = TRUE, all.x = TRUE)
OTH <- merge(OTH,OTH5, all.y = TRUE, all.x = TRUE)

# Add new columns to OTH for the BORE, LAT and LONG. Then use \'merge\' as a vlookup to add the corresponding
# bore and location from the arc file. The WALS and OTH files are slightly different because the arc file has
# a different licence number added in. 

OTH <- data.frame(OTH, BORE = \\"\\", LAT = \\"\\", LONG = \\"\\")

OTH$BORE <- arc$WORK_NO[match(OTH$LICENSE.APPROVAL, arc$LICENSE)]
OTH$LAT <- arc$POINT_X[match(OTH$LICENSE.APPROVAL, arc$LICENSE)]
OTH$LONG <- arc$POINT_Y[match(OTH$LICENSE.APPROVAL, arc$LICENSE)]

# The same process for the WALS files. No merging because there is only one WALS file.

WALS <- data.frame(WALS, BORE = \\"\\", LAT = \\"\\", LONG = \\"\\")

WALS$BORE <- arc$WORK_NO[match(WALS$LINKED.TO.WA.CA, arc$LICENSE)]
WALS$LAT <- arc$POINT_X[match(WALS$LINKED.TO.WA.CA, arc$LICENSE)]
WALS$LONG <- arc$POINT_Y[match(WALS$LINKED.TO.WA.CA, arc$LICENSE)]

# Merging of the WALS and OTH files. 

ALL <- merge(OTH, WALS, all.y = TRUE, all.x = TRUE)

# Conversion to new dataset format. 

new.WALS <- data.frame(LICENSE.APPROVAL = ALL$LICENSE.APPROVAL, 
                    BORE = ALL$BORE, 
                    HYDROCODE = \\"\\",               # Hydrocodes and Countbores I couldn\'t get working.
                    COUNTBORES = \\"\\" ,             # This was done in Excel.
                    STATUS  = ALL$STATUS,
                    CATEGORY= ALL$CATEGORY,
                    LINKED.TO.WA.CA = ALL$LINKED.TO.WA.CA,
                    LINKED.TO.AL= ALL$LINKED.TO.AL,
                    WATER.SHARING.PLAN = ALL$WATER.SHARING.PLAN,
                    WATER.SOURCE = ALL$WATER.SOURCE,
                    WATER.MANAGEMENT.ZONE = ALL$WATER.MANAGEMENT.ZONE,
                    PURPOSE= ALL$PURPOSE ,
                    SHARE.COMPONENT = ALL$SHARE.COMPONENT , 
                    ENTITLEMENT= ALL$ENTITLEMENT, 
                    ALLOCATION= ALL$ALLOCATION, 
                    VOL.PER.BORE = \\"\\",            # I couldn\'t get working either.
                    LAT = ALL$LAT, 
                    LONG = ALL$LONG, check.names= TRUE )


# Exporting out to *.csv

newWALS.location = paste(newWALS.folder ,\\"/\\",  newWALS.file, sep = \\"\\")
write.csv(new.WALS, file = newWALS.location)"""
                    }
                }
            }
        }
    }, 
    "gmd:metadataConstraints": None
}
