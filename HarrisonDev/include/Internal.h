//=============================================================================
// Copyright � 2008 Point Grey Research, Inc. All Rights Reserved.
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

#ifndef PGR_FC2_FLYCAPTURE2_INTERNAL_H
#define PGR_FC2_FLYCAPTURE2_INTERNAL_H

namespace FlyCapture2
{
	class InternalImp;

	class FLYCAPTURE2_API Internal
	{
		public:
			static void* GetInternal(unsigned int index);

		private:
			Internal(){}; // prevent class instantiation
			static InternalImp* m_pImpl;
	};
}

#endif // PGR_FC2_FLYCAPTURE2_INTERNAL_H
