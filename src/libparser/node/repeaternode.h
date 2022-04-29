/***************************************************************************
 * Copyright (C) 2019 by Renaud Guezennec                                   *
 * http://www.rolisteam.org/contact                      *
 *                                                                          *
 *  This file is part of DiceParser                                         *
 *                                                                          *
 * DiceParser is free software; you can redistribute it and/or modify       *
 * it under the terms of the GNU General Public License as published by     *
 * the Free Software Foundation; either version 2 of the License, or        *
 * (at your option) any later version.                                      *
 *                                                                          *
 * This program is distributed in the hope that it will be useful,          *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of           *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the             *
 * GNU General Public License for more details.                             *
 *                                                                          *
 * You should have received a copy of the GNU General Public License        *
 * along with this program; if not, write to the                            *
 * Free Software Foundation, Inc.,                                          *
 * 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.                 *
 ***************************************************************************/
#ifndef REPEATER_NODE_H
#define REPEATER_NODE_H

#include "node/executionnode.h"
#include <memory>

class RepeaterNode : public ExecutionNode
{
public:
    RepeaterNode();
    void run(ExecutionNode* previous) override;
    virtual QString toString(bool withLabel) const override;
    virtual qint64 getPriority() const override;

    virtual ExecutionNode* getCopy() const override;

    void setCommand(const std::vector<ExecutionNode*>& node);
    void setTimeNode(ExecutionNode* times);
    void setSumAll(bool b);

private:
    std::vector<ExecutionNode*> m_cmd;
    ExecutionNode* m_times= nullptr;
    bool m_sumAll= false;
};

#endif // REPEATER_NODE_H
