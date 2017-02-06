//=============================================================================
// Copyright © 2010 Point Grey Research, Inc. All Rights Reserved.
//
// This software is the confidential and proprietary information of Point
// Grey Research, Inc. ("Confidential Information").  You shall not
// disclose such Confidential Information and shall use it only in
// accordance with the terms of the license agreement you entered into
// with Point Grey Research, Inc. (PGR).
//
// PGR MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE
// SOFTWARE, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE, OR NON-INFRINGEMENT. PGR SHALL NOT BE LIABLE FOR ANY DAMAGES
// SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
// THIS SOFTWARE OR ITS DERIVATIVES.
//=============================================================================

//=============================================================================
// $Id: GCCamera.h 133799 2011-11-02 22:53:12Z rang $
//=============================================================================

#ifndef PGR_FC2_GCCAMERA_H_
#define PGR_FC2_GCCAMERA_H_

#include "CameraBase.h"
#include <GenApi/GenApi.h>
#include "BusManager.h"
#include "Camera.h"
#include "GigECamera.h"

using namespace ::GenApi;

namespace FlyCapture2
{
	class FLYCAPTURE2_API GCCamera : public CameraBase
	{
		public:
			GCCamera(void);
			virtual ~GCCamera(void);
			::GenApi::INodeMap* GetNodeMap();
			Error SetCamera( CameraBase* camera );
			Error SetCamera( CameraBase* camera, const char* filepath = NULL);
			std::string GCCamera::GetXML();

			/*@}*/

			virtual Error WriteGVCPRegister(
					unsigned int address,
					unsigned int value,
					bool broadcast = false);

			virtual Error ReadGVCPRegister(
					unsigned int address,
					unsigned int* pValue );

			virtual Error WriteGVCPRegisterBlock(
					unsigned int address,
					const unsigned int* pBuffer,
					unsigned int length );

			virtual Error ReadGVCPRegisterBlock(
					unsigned int address,
					unsigned int* pBuffer,
					unsigned int length );

			virtual Error WriteGVCPMemory(
					unsigned int address,
					const unsigned char* pBuffer,
					unsigned int length );

			virtual Error ReadGVCPMemory(
					unsigned int address,
					unsigned char* pBuffer,
					unsigned int length );

			/**
			 * The following functions are inherited from CameraBase. See
			 * CameraBase.h for further information.
			 */

			virtual Error Connect( PGRGuid* pGuid = NULL );
			Error Connect( PGRGuid* pGuid = NULL, const char* filepath = NULL);
			virtual Error Disconnect();
			virtual bool IsConnected();
			virtual Error SetCallback(
					ImageEventCallback callbackFn,
					const void* pCallbackData = NULL );
			virtual Error StartCapture(
					ImageEventCallback callbackFn = NULL,
					const void* pCallbackData = NULL );
			static Error StartSyncCapture(
					unsigned int numCameras,
					const GigECamera **ppCameras,
					const ImageEventCallback *pCallbackFns = NULL,
					const void** pCallbackDataArray = NULL );
			virtual Error RetrieveBuffer( Image* pImage );
			virtual Error StopCapture();
			virtual Error WaitForBufferEvent( Image* pImage, unsigned int eventNumber );
			virtual Error SetUserBuffers(
					unsigned char* const pMemBuffers,
					int size,
					int numBuffers );
			virtual Error GetConfiguration( FC2Config* pConfig );
			virtual Error SetConfiguration( const FC2Config* pConfig );
			virtual Error GetCameraInfo( CameraInfo* pCameraInfo );
			virtual Error GetPropertyInfo( PropertyInfo* pPropInfo );
			virtual Error GetProperty( Property* pProp );
			virtual Error SetProperty(
					const Property* pProp,
					bool broadcast = false );
			virtual Error GetGPIOPinDirection( unsigned int pin, unsigned int* pDirection);
			virtual Error SetGPIOPinDirection( unsigned int pin, unsigned int direction, bool broadcast = false );
			virtual Error GetTriggerModeInfo( TriggerModeInfo* pTriggerModeInfo );
			virtual Error GetTriggerMode( TriggerMode* pTriggerMode );
			virtual Error SetTriggerMode(
					const TriggerMode* pTriggerMode,
					bool broadcast = false );
			virtual Error FireSoftwareTrigger( bool broadcast = false );
			virtual Error GetTriggerDelayInfo( TriggerDelayInfo* pTriggerDelayInfo );
			virtual Error GetTriggerDelay( TriggerDelay* pTriggerDelay );
			virtual Error SetTriggerDelay(
					const TriggerDelay* pTriggerDelay,
					bool broadcast = false );
			virtual Error GetStrobeInfo( StrobeInfo* pStrobeInfo );
			virtual Error GetStrobe( StrobeControl* pStrobeControl );
			virtual Error SetStrobe(
					const StrobeControl* pStrobeControl,
					bool broadcast = false );
			virtual Error GetLUTInfo( LUTData* pData );
			virtual Error GetLUTBankInfo(
					unsigned int bank,
					bool* pReadSupported,
					bool* pWriteSupported );
			virtual Error GetActiveLUTBank( unsigned int* pActiveBank );
			virtual Error SetActiveLUTBank( unsigned int activeBank );
			virtual Error EnableLUT( bool on );
			virtual Error GetLUTChannel(
					unsigned int bank,
					unsigned int channel,
					unsigned int sizeEntries,
					unsigned int* pEntries );
			virtual Error SetLUTChannel(
					unsigned int bank,
					unsigned int channel,
					unsigned int sizeEntries,
					const unsigned int* pEntries );
			virtual Error GetMemoryChannel( unsigned int* pCurrentChannel );
			virtual Error SaveToMemoryChannel( unsigned int channel );
			virtual Error RestoreFromMemoryChannel( unsigned int channel );
			virtual Error GetMemoryChannelInfo( unsigned int* pNumChannels );
			virtual Error GetEmbeddedImageInfo( EmbeddedImageInfo* pInfo );
			virtual Error SetEmbeddedImageInfo( EmbeddedImageInfo* pInfo );
			virtual Error WriteRegister(
					unsigned int address,
					unsigned int value,
					bool broadcast=false);
			virtual Error ReadRegister(
					unsigned int address,
					unsigned int* pValue );
			virtual Error WriteRegisterBlock(
					unsigned short addressHigh,
					unsigned int addressLow,
					const unsigned int* pBuffer,
					unsigned int length );
			virtual Error ReadRegisterBlock(
					unsigned short addressHigh,
					unsigned int addressLow,
					unsigned int* pBuffer,
					unsigned int length );
			static const char* GetRegisterString( unsigned int registerVal);
			Error GetCycleTime(TimeStamp *timeStamp);
			InterfaceType GetInterfaceType();
			virtual Error GetStats( CameraStats* pStats );
			virtual Error ResetStats();

	protected:
			BusManager m_busMgr;
			void TestGainNode();
	private:
			InterfaceType m_type;

			Error LoadXML(const char* filepath = NULL);
			Error UncompressGenICamXML( std::string &aData );
};
}
#endif
