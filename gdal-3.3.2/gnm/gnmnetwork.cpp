/******************************************************************************
 *
 * Project:  GDAL/OGR Geography Network support (Geographic Network Model)
 * Purpose:  GNM network class.
 * Authors:  Mikhail Gusev (gusevmihs at gmail dot com)
 *           Dmitry Baryshnikov, polimax@mail.ru
 *
 ******************************************************************************
 * Copyright (c) 2014, Mikhail Gusev
 * Copyright (c) 2014-2015, NextGIS <info@nextgis.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 ****************************************************************************/

#include "gnm_api.h"
#include "ogrsf_frmts.h"

CPL_CVSID("$Id: gnmnetwork.cpp 8e5eeb35bf76390e3134a4ea7076dab7d478ea0e 2018-11-14 22:55:13 +0100 Even Rouault $")

GNMNetwork::GNMNetwork() : GDALDataset() {}

GNMNetwork::~GNMNetwork() {}

const char *GNMNetwork::GetName() const
{
    return m_soName;
}

//! @cond Doxygen_Suppress
const char *GNMNetwork::_GetProjectionRef()
{
    return m_soSRS;
}
//! @endcond

char **GNMNetwork::GetFileList()
{
    return nullptr;
}

//--- C API --------------------------------------------------------------------

const char* CPL_STDCALL GNMGetName (GNMNetworkH hNet)
{
    VALIDATE_POINTER1( hNet, "GNMGetVersion", nullptr );

    return ((GNMNetwork*)hNet)->GetName();
}

int CPL_STDCALL GNMGetVersion(GNMNetworkH hNet)
{
    VALIDATE_POINTER1( hNet, "GNMGetVersion", 0 );

    return ((GNMNetwork*)hNet)->GetVersion();
}

CPLErr CPL_STDCALL GNMDisconnectAll (GNMNetworkH hNet)
{
    VALIDATE_POINTER1( hNet, "GNMDisconnectAll", CE_Failure );

    return ((GNMNetwork*)hNet)->DisconnectAll();
}

OGRFeatureH CPL_STDCALL GNMGetFeatureByGlobalFID (GNMNetworkH hNet, GNMGFID nGFID)
{
    VALIDATE_POINTER1( hNet, "GNMGetFeatureByGlobalFID", nullptr );

    return (OGRFeatureH) ((GNMNetwork*)hNet)->GetFeatureByGlobalFID(nGFID);
}

OGRLayerH CPL_STDCALL GNMGetPath (GNMNetworkH hNet, GNMGFID nStartFID,
                              GNMGFID nEndFID, GNMGraphAlgorithmType eAlgorithm,
                              char** papszOptions)
{
    VALIDATE_POINTER1( hNet, "GNMGetPath", nullptr );

    return (OGRLayerH) ((GNMNetwork*)hNet)->GetPath(nStartFID, nEndFID,
                                                    eAlgorithm, papszOptions);
}

GNMNetworkH CPL_STDCALL GNMCastToNetwork(GDALMajorObjectH hBase)
{
    return reinterpret_cast<GNMNetworkH>(
        dynamic_cast<GNMNetwork*>(reinterpret_cast<GDALMajorObject*>(hBase)));
}

GNMGenericNetworkH CPL_STDCALL GNMCastToGenericNetwork(GDALMajorObjectH hBase)
{
    return reinterpret_cast<GNMGenericNetworkH>(
        dynamic_cast<GNMNetwork*>(reinterpret_cast<GDALMajorObject*>(hBase)));
}