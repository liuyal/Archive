
#ifndef Sender_SS_H
#define Sender_SS_H

#include <ss_api.hxx>

/*Context*/
class SenderX;

namespace Sender_SS
{
	using namespace smartstate;
	//State Mgr
	// Commented out and put in SenderSS-class.h
	//State Mgr
	class SenderSS : public StateMgr
	{
		public:
			SenderSS(SenderX* ctx, bool startMachine=true);

			SenderX& getCtx() const;

		private:
			SenderX* myCtx;
	};

	//Base State
	class SenderBaseState : public BaseState
	{
		protected:
			SenderBaseState(){};
			SenderBaseState(const string& name, BaseState* parent, SenderSS* mgr);

		protected:
			SenderSS* getMgr(){return static_cast<SenderSS*>(myMgr);}
	};

	//States
	//------------------------------------------------------------------------
	class Sender_TopLevel_SenderSS : public virtual SenderBaseState
	{
			typedef SenderBaseState super;

		public:
			Sender_TopLevel_SenderSS(){};
			Sender_TopLevel_SenderSS(const string& name, BaseState* parent, SenderSS* mgr);

			virtual void onMessage(const Mesg& mesg);

			virtual void onEntry();
			virtual void onExit();

		//Transitions

		private:
			void onSERMessage(const Mesg& mesg);
	};

	class ACKNAK_Sender_TopLevel : public virtual Sender_TopLevel_SenderSS
	{
			typedef Sender_TopLevel_SenderSS super;

		public:
			ACKNAK_Sender_TopLevel(){};
			ACKNAK_Sender_TopLevel(const string& name, BaseState* parent, SenderSS* mgr);

			virtual void onMessage(const Mesg& mesg);

			virtual void onEntry();
			virtual void onExit();

		//Transitions

		private:
			void onSERMessage(const Mesg& mesg);
	};

	class EOT1_Sender_TopLevel : public virtual Sender_TopLevel_SenderSS
	{
			typedef Sender_TopLevel_SenderSS super;

		public:
			EOT1_Sender_TopLevel(){};
			EOT1_Sender_TopLevel(const string& name, BaseState* parent, SenderSS* mgr);

			virtual void onMessage(const Mesg& mesg);

			virtual void onEntry();
			virtual void onExit();

		//Transitions

		private:
			void onSERMessage(const Mesg& mesg);
	};

	class START_Sender_TopLevel : public virtual Sender_TopLevel_SenderSS
	{
			typedef Sender_TopLevel_SenderSS super;

		public:
			START_Sender_TopLevel(){};
			START_Sender_TopLevel(const string& name, BaseState* parent, SenderSS* mgr);

			virtual void onMessage(const Mesg& mesg);

			virtual void onEntry();
			virtual void onExit();

		//Transitions

		private:
			void onSERMessage(const Mesg& mesg);
	};

	class EOTEOT_Sender_TopLevel : public virtual Sender_TopLevel_SenderSS
	{
			typedef Sender_TopLevel_SenderSS super;

		public:
			EOTEOT_Sender_TopLevel(){};
			EOTEOT_Sender_TopLevel(const string& name, BaseState* parent, SenderSS* mgr);

			virtual void onMessage(const Mesg& mesg);

			virtual void onEntry();
			virtual void onExit();

		//Transitions

		private:
			void onSERMessage(const Mesg& mesg);
	};

	class CAN_Sender_TopLevel : public virtual Sender_TopLevel_SenderSS
	{
			typedef Sender_TopLevel_SenderSS super;

		public:
			CAN_Sender_TopLevel(){};
			CAN_Sender_TopLevel(const string& name, BaseState* parent, SenderSS* mgr);

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
