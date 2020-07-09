
#ifndef Receiver_SS_H
#define Receiver_SS_H

#include <ss_api.hxx>

/*Context*/
class ReceiverX;

namespace Receiver_SS
{
	using namespace smartstate;
	//State Mgr
	// Commented out and put in ReceiverSS-class.h
	//State Mgr
	class ReceiverSS : public StateMgr
	{
		public:
			ReceiverSS(ReceiverX* ctx, bool startMachine=true);

			ReceiverX& getCtx() const;

		private:
			ReceiverX* myCtx;
	};

	//Base State
	class ReceiverBaseState : public BaseState
	{
		protected:
			ReceiverBaseState(){};
			ReceiverBaseState(const string& name, BaseState* parent, ReceiverSS* mgr);

		protected:
			ReceiverSS* getMgr(){return static_cast<ReceiverSS*>(myMgr);}
	};

	//States
	//------------------------------------------------------------------------
	class Receiver_TopLevel_ReceiverSS : public virtual ReceiverBaseState
	{
			typedef ReceiverBaseState super;

		public:
			Receiver_TopLevel_ReceiverSS(){};
			Receiver_TopLevel_ReceiverSS(const string& name, BaseState* parent, ReceiverSS* mgr);

			virtual void onMessage(const Mesg& mesg);

			virtual void onEntry();
			virtual void onExit();

		//Transitions

		private:
			void onSERMessage(const Mesg& mesg);
	};

	class FirstByte_Receiver_TopLevel : public virtual Receiver_TopLevel_ReceiverSS
	{
			typedef Receiver_TopLevel_ReceiverSS super;

		public:
			FirstByte_Receiver_TopLevel(){};
			FirstByte_Receiver_TopLevel(const string& name, BaseState* parent, ReceiverSS* mgr);

			virtual void onMessage(const Mesg& mesg);

			virtual void onEntry();
			virtual void onExit();

		//Transitions

		private:
			void onSERMessage(const Mesg& mesg);
	};

	class EOT_Receiver_TopLevel : public virtual Receiver_TopLevel_ReceiverSS
	{
			typedef Receiver_TopLevel_ReceiverSS super;

		public:
			EOT_Receiver_TopLevel(){};
			EOT_Receiver_TopLevel(const string& name, BaseState* parent, ReceiverSS* mgr);

			virtual void onMessage(const Mesg& mesg);

			virtual void onEntry();
			virtual void onExit();

		//Transitions

		private:
			void onSERMessage(const Mesg& mesg);
	};

	class ConditionalTransient_Receiver_TopLevel : public virtual Receiver_TopLevel_ReceiverSS
	{
			typedef Receiver_TopLevel_ReceiverSS super;

		public:
			ConditionalTransient_Receiver_TopLevel(){};
			ConditionalTransient_Receiver_TopLevel(const string& name, BaseState* parent, ReceiverSS* mgr);

			virtual void onMessage(const Mesg& mesg);

			virtual void onEntry();
			virtual void onExit();

		//Transitions

		private:
			void onCONTMessage(const Mesg& mesg);
	};

	class CAN_Receiver_TopLevel : public virtual Receiver_TopLevel_ReceiverSS
	{
			typedef Receiver_TopLevel_ReceiverSS super;

		public:
			CAN_Receiver_TopLevel(){};
			CAN_Receiver_TopLevel(const string& name, BaseState* parent, ReceiverSS* mgr);

			virtual void onMessage(const Mesg& mesg);

			virtual void onEntry();
			virtual void onExit();

		//Transitions

		private:
			void onSERMessage(const Mesg& mesg);
	};

};

#endif

//___________________________________vv^^vv___________________________________
