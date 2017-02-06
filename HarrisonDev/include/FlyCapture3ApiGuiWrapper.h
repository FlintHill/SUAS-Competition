//=============================================================================
// Copyright © 2013 Point Grey Research, Inc. All Rights Reserved.
//
// This software is the confidential and proprietary information of Point
// Grey Research, Inc. ("Confidential Information").  You shall not
// disclose such Confidential Information and shall use it only in
// accordance with the terms of the license agreement you entered into
// with PGR.
//
// PGR MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE
// SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
// IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE, OR NON-INFRINGEMENT. PGR SHALL NOT BE LIABLE FOR ANY DAMAGES
// SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
// THIS SOFTWARE OR ITS DERIVATIVES.
//=============================================================================

#pragma once


#include "StdAfx.h"
#include <vcclr.h>
#include <List>
#using <mscorlib.dll>
#include "FlyCapture2.h"
#include "GCCamera.h"
#using <System.dll>
#using "PresentationFramework.dll"
#using "PresentationCore.dll"
#using "WindowsBase.dll"

using namespace System::Threading;
using namespace System;
using namespace System::Windows;
using namespace System::Windows::Controls;

#ifdef _DEBUG
#if _MSC_VER == 1600
#using <..\\..\\bin\\FlyCapture2Managedd_v100.dll>
#using <..\\..\\bin\\FlyCapture2d_v100.dll>
#using <..\\..\\bin\\FlyCap3CameraControld_v100.dll> as_friend
#elif _MSC_VER == 1500
#using <..\\..\\bin\\FlyCapture2d_v90.dll>
#using <..\\..\\bin\\FlyCap3CameraControld_v90.dll> as_friend
#else
#using <..\\..\\bin\\FlyCapture2d.dll>
#using <..\\..\\bin\\FlyCap3CameraControld.dll> as_friend

#endif

#else
#if _MSC_VER == 1600
#using <..\\..\\bin\\FlyCapture2Managed_v100.dll>
//#using <..\\..\\bin\\FlyCapture2_v100.dll>
#using <..\\..\\bin\\FlyCap3CameraControl_v100.dll> as_friend
#elif _MSC_VER == 1500
#using <..\\..\\bin\\FlyCapture2_v90.dll>
#using <..\\..\\bin\\FlyCap3CameraControl_v90.dll> as_friend
#else
#using <..\\..\\bin\\FlyCapture2.dll>
#using <..\\..\\bin\\FlyCap3CameraControl.dll> as_friend
#endif
#endif

#ifdef WRAPPER_EXPORTS
#define WRAPPER_API __declspec(dllexport)
#else
#define WRAPPER_API __declspec(dllimport)
#endif

using namespace FlyCap3CameraControl;
namespace FlyCapture2
{
	class CameraBase;
}

namespace FlyCap3CameraControl
{
	class FlyCapture3ApiGuiWrapper
	{
		public:
			WRAPPER_API FlyCapture3ApiGuiWrapper(void);
			WRAPPER_API ~FlyCapture3ApiGuiWrapper(void);
			WRAPPER_API void ConnectGUILibrary(FlyCapture2::GCCamera& camera);
			WRAPPER_API void DisconnectGUILibrary();
			WRAPPER_API void ShowPropertyGridDialog();
			WRAPPER_API void ShowCameraSelectionDialog();
			WRAPPER_API int GetNumDialogs();
			WRAPPER_API std::list<std::string> GetDialogNameList();
			WRAPPER_API void ShowDialogByName(std::string dialogName);
			WRAPPER_API void ShowDialogByIndex(int index);
			WRAPPER_API int GetNumOfControls();
			WRAPPER_API std::list<std::string> GetControlNameList();
		private:
			gcroot<FlyCap3CameraControl::GUIFactory^> m_pGuiFactory;
	};
}
