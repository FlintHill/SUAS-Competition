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
// $Id: NodeMap.h 133799 2011-11-02 22:53:12Z rang $
//=============================================================================

#ifndef PGR_FC2_NODEMAP_H_
#define PGR_FC2_NODEMAP_H_

#include <GenApi/GenApi.h>

using namespace GenICam;
using namespace GenApi;

namespace FlyCapture2
{
	class NodeMap
	{
		public:
			NodeMap(GenApi::CNodeMapRef *ref);
			virtual ~NodeMap(void);

			//! Get device name
			GenICam::gcstring _GetDeviceName();

			//! Fires nodes which have a polling time
			void _Poll( int64_t ElapsedTime );

			//! Retrieves all nodes in the node map
			void _GetNodes(NodeList_t &Nodes);

			//! Retrieves the node from the central map by name
			INode* _GetNode( const GenICam::gcstring& key);

			//! Invalidates all nodes
			void _InvalidateNodes() const;

		private:
			GenApi::CNodeMapRef *mNodeMapRef;
	};
}

#endif
